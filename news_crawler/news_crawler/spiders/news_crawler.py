# -*- coding: utf-8 -*-

import scrapy
from news_crawler.items import NewsCrawlerItem
from scrapy.loader import ItemLoader

class newsSpider(scrapy.Spider):
    name = 'news_crawler'
        
    def start_requests(self):
        for i in range(1,500):
            yield scrapy.Request('https://markets.businessinsider.com/news/ressort/commodities?p=%s' % i, callback=self.parse)
            
    def parse(self, response):
        for row in response.xpath("//table[@class='table table-small'][1]/tbody/tr"):
            l = ItemLoader(item = NewsCrawlerItem(), selector = row)
            l.add_xpath('DateTime','td[1]')
            l.add_xpath("News", 'td[2]/a/text()')
                        
            yield l.load_item()