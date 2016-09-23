from xml.etree.ElementTree import fromstring
import scrapy
import psycopg2
from bookcrawler.items import BookItem, BookCategoryItem
import settings
import urllib
import re

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["naver.com"]
    start_urls = [
        "http://book.naver.com/",
    ]

    client_id = 'z0vmzY41HNFZChG9KNr9'
    client_secret = 'QYkMjdzpz6'

    def parse(self, response):
        conn = psycopg2.connect(settings.DBSETTINGS())
        cur = conn.cursor()
        cur.execute("""select * from categories;""")
        rows = cur.fetchall()

        # row = rows[0]
        for row in rows:
            for i in range(1,1001):
                yield scrapy.Request(url="https://openapi.naver.com/v1/search/book_adv.xml?d_cont=1&start="+str(i)+"&display=100&d_catg="+str(row[0]),
                    headers={'X-Naver-Client-Id':self.client_id,'X-Naver-Client-Secret':self.client_secret,
                        'Accept':'*/*', 'Content-Type': 'application/xml'},
                        callback=self.parseXML)


    def parseXML(self, response):
        bitem = BookItem()
        tree = fromstring(response.body).find('channel')
        count = tree.find("total")
        items = tree.findall("item")
        for item in items:
            burl = urllib.urlopen(unicode(item.find("link").text)).geturl()
            bid = re.search('(?<=bid=)\d+',burl).group(0)
            bitem['bid'] = bid
            bitem['Title'] = item.find("title").text.replace('<b>','').replace('</b>','').replace("'","''")
            bitem['ISBN'] = item.find("isbn").text
            bitem['Author'] = item.find("author").text
            bitem['Publisher'] = item.find("publisher").text
            bitem['Primere'] = item.find("pubdate").text
            if item.find("image") is not None:
                bitem['Cover'] = item.find("image").text
            else:
                bitem['Cover'] = "/static/images/noimage.jpg"
            bitem['Link'] = burl

            conn = psycopg2.connect(settings.DBSETTINGS())
            cur = conn.cursor()
            cur.execute("""INSERT INTO books ("id", "isbn", "title", "author", "publisher","primere","cover","link","createdAt","updatedAt")
                        VALUES ('%(bid)s', '%(ISBN)s', '%(Title)s', '%(Author)s', '%(Publisher)s',
                            '%(Primere)s', '%(Cover)s', '%(Link)s', now(), now());"""%dict(bitem))
            conn.commit()

            yield scrapy.Request(url=burl, callback=self.parseCategory)

    def parseCategory(self,response):
        bcitem = BookCategoryItem()
        bcitem['Book'] = re.search('(?<=bid=)\d+',response.url).group(0)

        conn = psycopg2.connect(settings.DBSETTINGS())
        for genre in response.xpath('//ul[@class="history"]/li'):
            bcitem['Category'] = (genre.xpath('substring-after(./a[position()=3]/@href, "cate_code=")').extract())[0]
            if bcitem['Category'] != "":
                cur = conn.cursor()
                cur.execute("""INSERT INTO book_category ("bookId", "categoryId", "createdAt","updatedAt")
                            VALUES ('%s', '%s', now(), now());"""%
                            (bcitem['Book'],bcitem['Category']))
        conn.commit()