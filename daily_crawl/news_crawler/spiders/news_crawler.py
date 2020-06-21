# -*- coding: utf-8 -*-

import scrapy
from news_crawler.items import NewsCrawlerItem
from scrapy.loader import ItemLoader

class newsSpider(scrapy.Spider):
    name = 'news_crawler'
        
    def start_requests(self):
        for i in range(1,60):
            yield scrapy.Request('https://markets.businessinsider.com/commodities/news/oil-price?type=wti&p=%s' % i, callback=self.parse)
            
    def parse(self, response):
        for row in response.xpath(r"//div[@class='col-md-6 further-news-container latest-news-padding']"):
            l = ItemLoader(item = NewsCrawlerItem(), selector = row)
            l.add_xpath("DateTime", r"div/div/span[@class='warmGrey source-and-publishdate']/text()[2]")
            l.add_xpath("News", r"div/div/a[@class='news-link']/text()")
                        
            yield l.load_item()