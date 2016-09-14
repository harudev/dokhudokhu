# -*- coding: utf-8 -*-
import scrapy
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
from bookcrawler.items import BookscrapItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["kyobobook.co.kr"]
    start_urls = [
        "http://www.kyobobook.co.kr/indexKor.laf",
    ]

    def parse(self, response):    
        root = response.xpath('//div[@class="nav_category"]')
        for url in root.xpath('./ul/li/a/@href'):
            yield scrapy.Request(url.extract(),callback=self.parse2)

    def parse2(self, response):
        root = response.xpath('//div[@class="nav_category"]')
        for cat in root.xpath('./ul/li'):
                for subcat in cat.xpath('./ul//li'):
                    conn = psycopg2.connect("dbname='dokhudokhu' user='ruci' host='localhost' password='13579'")

                    cur = conn.cursor()
                    Cat = subcat.xpath('./a/text()').extract()[0]
                    query = u'SELECT id from book_category Where "Third"=\'%s\';'%Cat
                    cur.execute(query)
                    idnum = cur.fetchone()[0]
                    newurl = response.urljoin(subcat.xpath('./a/@href').extract()[0])
                    request = scrapy.Request(newurl,callback=self.parse3)
                    request.meta['idnum'] = idnum
                    yield request
                    
    def parse3(self,response):
        oldurl = response.request.url
        linkClass = oldurl.split("linkClass=")[1]
        url = "http://www.kyobobook.co.kr/category/search/SearchCategoryMain.jsp/linkClass="+linkClass[0:6]+"&mallGb=KOR&tabName=SearchAll&targetPage=&sortColumn="
        request = scrapy.Request(url,callback=self.parse4,method="POST",
            headers={'Content-Type':'application/x-www-form-urlencoded',
                    'Host':'www.kyobobook.co.kr',
                    'Origin': 'http://www.kyobobook.co.kr',
                    'Upgrade-Insecure-Requests': '1',
                    'Accept-Encoding': 'gzip, deflate',
            })
        #request.meta['idnum'] = response.meta['idnum']
        yield request

    def parse4(self,response):
        print "PARSE44444444444444444444444444"
        for link in response.xpath('//dl[@class="book_title"]/dt/strong/a/@href').extract():
            print link
            #for sublink in link.xpath('./dl').extract():
                #print sublink
             #//dl[@class="book_title"]/dt/strong/a/@href
            # print link
            # print "linked@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2"
            # link = link[0].split("'")
            # print link[5]
            # print link[6]
            # link = link[5]
            # request = scrapy.Request('http://www.kyobobook.co.kr/product/detailViewKor.laf?barcode='+link,callback=self.parse4)
            # request.meta['idnum'] = response.meta['idnum']
            # request.meta['isbn'] = link
            # yield request
        

    def parse5(self, response):
        item = BookscrapItem()
        item['Category'] = response.meta['idnum']
        item['ISBN'] = response.meta['isbn']
        item['Title'] = response.xpath('normalize-space(//h1[@class="title"]/strong/text())').extract()
        item['Subtitle'] = response.xpath('normalize-space(//div[@class="box_detail_point"]/div[@class="info"]/text())').extract()
        item['Author'] = response.xpath('normalize-space(//div[@class="author"]/span[@class="name"@title=""]/text())').extract()
        item['Publish'] = response.xpath('normalize-space(//div[@class="author"]/span[@class="name"]/a/text())').extract()
        item['Date'] = response.xpath('normalize-space(//div[@class="author"]/span[@class="name"@title="출간일"]/text())').extract()
        item['Cover'] = response.xpath('div[@class="cover"]/a/img/@src').extract()
        item['Description'] = response.xpath('normalize-space(div[@class="box_detail_article"]/text())').extract()

        conn = psycopg2.connect("dbname='dokhudokhu' user='ruci' host='localhost' password='13579'")
        cur = conn.cursor()

        cur.execute("""INSERT INTO book_book ("Category", "ISBN", "Title", "Subtitle", "Author", "Publish", "Date", "Cover","Description")
                        VALUES (%(Category)s, %(ISBN)s, %(Title)s, %(Subtitle)s, %(Author)s, %(Publish)s, %(Date)s, %(Cover)s, %(Description)s);""",
                        dict(item))
        conn.commit()