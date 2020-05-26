# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# Execute with :
#       scrapy crawl news_crawler -o ..\output\news.csv
# In news_crawler directory



import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def remove_whitespace(value):
    return value.strip()


class NewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    News = scrapy.Field(
            input_processor = MapCompose(remove_tags,remove_whitespace),
            output_processor = TakeFirst()
            )
    
    DateTime = scrapy.Field(
            input_processor = MapCompose(remove_tags,remove_whitespace),
            output_processor = TakeFirst()
            )

