import scrapy
import psycopg2
from bookcrawler.items import BookItem, BookCategoryItem
import settings

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["naver.com"]
    start_urls = [
        "book.naver.com",
    ]

    client_id = 'z0vmzY41HNFZChG9KNr9'
    client_secret = 'QYkMjdzpz6'

    def parse(self, response):
        conn = psycopg2.connect(settings.DBSETTINGS())

        cur = conn.cursor()
        cur.execute("""select * from categories;""")
        rows = cur.fetchall()

        for row in rows:
            yield scrapy.Request(url="https://openapi.naver.com/v1/search/book_adv.xml?d_cont=1&display=100&d_catg="+row[0],
                        headers={'X-Naver-Client-Id':client_id,'X-Naver-Client-Secret':client_secret,
                            'Accept':'*/*', 'Content-Type': 'application/xml'},
                            callback=self.parseXML)

    def parseXML(self, response):
        root = response.xpath()
        print response
