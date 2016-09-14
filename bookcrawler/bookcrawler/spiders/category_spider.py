import scrapy
import psycopg2
from bookcrawler.items import CategoryItem

class CategorySpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["naver.com"]
    start_urls = [
        "http://book.naver.com/",
    ]

    def parse(self, response):
        try:
            root = response.xpath('//div[@id="left_category"]')
    #        print repr(root.extract()).decode("unicode-escape")
            for code in root.xpath('.//ul//li/a/@cate').extract():
                url = "http://book.naver.com/category/index.nhn?cate_code=" + code
                yield scrapy.Request(url,callback=self.parse2)
        except:
            print "Unable to get "

    def parse2(self, response):
        item = CategoryItem()
        item['First'] = response.xpath('//div[@class="location"]/h2/text()').extract()
        root = response.xpath('//div[@id="family_category"]')
        for cat in root.xpath('.//div[@class="category_detail_inner"]'):
                item['Second'] = cat.xpath('./h3/a/text()').extract()
                print unicode(item['Second'])
                for subcat in cat.xpath('.//ul//li'):
                    item['code'] = subcat.xpath('substring-after(./a/@href,"cate_code=")').extract()
                    item['Third'] = subcat.xpath('./a/text()').extract()
                    conn = psycopg2.connect("dbname='dokhudokhu' user='ruci' host='localhost' password='13579'")

                    cur = conn.cursor()

                    cur.execute("""INSERT INTO book_category ("First", "Second", "Third","BookCount")
                                    VALUES (%(First)s, %(Second)s, %(Third)s, 0);""",
                                    dict(item))
                    conn.commit()