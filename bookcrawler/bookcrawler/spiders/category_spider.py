import scrapy
import psycopg2
from bookcrawler.items import CategoryItem
import settings

class BookSpider(scrapy.Spider):
    name = "book"
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
            print "Unable to get pages"

    def parse2(self, response):
        item = CategoryItem()
        item['First'] = response.xpath('//div[@class="location"]/h2/text()').extract()
        root = response.xpath('//div[@id="family_category"]')
        for cat in root.xpath('.//div[@class="category_detail_inner"]'):
                item['Second'] = cat.xpath('./h3/a/text()').extract()
                for subcat in cat.xpath('.//ul//li'):
                    item['code'] = subcat.xpath('substring-after(./a/@href,"cate_code=")').extract()
                    item['Third'] = subcat.xpath('./a/text()').extract()
                    conn = psycopg2.connect(settings.DBSETTINGS())

                    cur = conn.cursor()
                    cur.execute("""INSERT INTO categories ("code", "first", "second", "third","bookCount","createdAt","updatedAt")
                                    VALUES ('%s', '%s', '%s', '%s', 0, now(), now());"""%
                                    (item['code'][0],item['First'][0],item['Second'][0],item['Third'][0]))
                    conn.commit()