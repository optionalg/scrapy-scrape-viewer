import scrapy
from expresspros.items import ExpressprosItem

import datetime

class ExpressprosSpider(scrapy.Spider):
    name = "expresspros"
    allowed_domain = ["https://www.expresspros.com/"]
    start_urls = ["https://workforce.expresspros.com/locations/state/Alabama"]

    # tutorial guidance: https://doc.scrapy.org/en/latest/intro/tutorial.html#more-examples-and-patterns

    # follow links to city pages
    def parse(self, response):
        for href in response.xpath('//div[@class="row location-item"][@style="padding-bottom: 15px;"]/div[2]/div[3]/a/@href'):
            yield response.follow(href, self.parse_city)

    # scrape the page the link led me to
    def parse_city(self, response):
        for sel in response.css('div.widgetBody > div.row'):
            yield {
                'title': sel.css('div.col-sm-7 h3::text').extract_first(),
                'url': sel.css('a.btn::attr(href)').extract_first(),
                'company': sel.css('div.col-sm-3 h3::text').extract_first().strip(),
                'date': datetime.datetime.now().strftime ("%Y%m%d")
            }
