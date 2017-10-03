import scrapy

class JobFairsInSpider(scrapy.Spider):
    name = 'jobfairsin'
    allowed_domain = ["http://jobfairsin.com"]
    #start_urls = [ 'http://jobfairsin.com/georgia' ]

    def __init__(self, domain='', *args,**kwargs):
        super(JobFairsInSpider, self).__init__(*args, **kwargs)
        self.start_urls = [domain]

    # tutorial guidance: https://doc.scrapy.org/en/latest/intro/tutorial.html#more-examples-and-patterns

    def parse(self, response):
        # scrape contact info
        for sel in response.css('#tiledGrid'):
            yield {

            }
