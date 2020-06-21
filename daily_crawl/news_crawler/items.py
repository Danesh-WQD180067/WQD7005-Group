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
from datetime import date, timedelta

def remove_whitespace(value):
    return value.strip()

# Assume that scraping is done at midnight
def get_date(value):
    if ("d" in value):
        value = value.replace('d', '')
        days_diff = int(value) + 1
        newsdate = date.today() - timedelta(days=days_diff)
    else:
         newsdate = date.today() - timedelta(days=1)
    return newsdate.strftime('%m/%d/%Y')

class NewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    News = scrapy.Field(
            input_processor = MapCompose(remove_tags,remove_whitespace),
            output_processor = TakeFirst()
            )
    
    DateTime = scrapy.Field(
            input_processor = MapCompose(remove_tags,remove_whitespace,get_date),
            output_processor = TakeFirst()
            )

