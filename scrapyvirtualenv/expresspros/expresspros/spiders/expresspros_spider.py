import scrapy
from expresspros.items import ExpressprosItem

import datetime

class ExpressprosSpider(scrapy.Spider):
    name = "expresspros"
    allowed_domain = ["https://www.expresspros.com/"]
    # start_urls = ["https://workforce.expresspros.com/locations/state/Alabama", "https://workforce.expresspros.com/locations/state/Georgia", "https://workforce.expresspros.com/locations/state/Florida"]

    # manually enter start url's and outputfiles
    # scrapy crawl expresspros -a domain='https://workforce.expresspros.com/locations/state/Alabama' -o ../../demo-csv-json-scrape/expresspros_Alabama_Videmo.json -t json
    def __init__(self, domain='', *args,**kwargs):
        '''
            Spider arguments are passed while running the crawl command using the -a option.
            You would use *args when you're not sure how many arguments might be passed to your function
            Similarly, **kwargs allows you to handle named arguments that you have not defined in advance

            For example:
            scrapy crawl myspider -a category='mycategory' -a domain='example.com'
            scrapy crawl expresspros -a domain='https://workforce.expresspros.com/locations/state/Alabama' -o myjsontest.json

            # https://stackoverflow.com/questions/15611605/how-to-pass-a-user-defined-argument-in-scrapy-spider
            # https://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments
        '''
        super(ExpressprosSpider, self).__init__(*args, **kwargs)
        self.start_urls = [domain]

    # tutorial guidance: https://doc.scrapy.org/en/latest/intro/tutorial.html#more-examples-and-patterns

    def parse(self, response):
        # scrape contact info
        for sel in response.xpath('//div[@class="row location-item"][@style="padding-bottom: 15px;"]'):
            item = ExpressprosItem()
            item['officeCity'] = sel.xpath('h4/text()').extract()
            item['officeAddress'] = sel.xpath('div/div/div/text()').extract()
            item['officePhone'] = sel.xpath('div[1]/div[2]/a/@href').extract()
            item['officeEmail'] = sel.xpath('div[2]/div[1]/a/@href').extract()
            item['officeWeb'] = sel.xpath('div[2]/div[2]/a/@href').extract()
            yield item

        # follow links to city pages
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
