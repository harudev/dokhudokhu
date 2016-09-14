# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CategoryItem(scrapy.Item):
	code = scrapy.Field()
	First = scrapy.Field()
	Second = scrapy.Field()
	Third = scrapy.Field()

class BookscrapItem(scrapy.Item):
	bid = scrapy.Field()
	ISBN = scrapy.Field()
	Title = scrapy.Field()
	SubTitle = scrapy.Field()
	Author = scrapy.Field()
	Publish = scrapy.Field()
	Date = scrapy.Field()
	Description = scrapy.Field()
	Cover = scrapy.Field()

class BookCategoryItem(scrapy.Item):
	Category = scrapy.Field()
	Book = scrapy.Field()