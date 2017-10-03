import scrapy

class JobUpsSpider(scrapy.Spider):
    name = 'jobfairsin'
    allowed_domain = ["hhttps://www.jobs-ups.com/"]
    #start_urls = [ 'https://www.jobs-ups.com/search-jobs/Florida' ]

    def __init__(self, domain='', *args,**kwargs):
        super(JobUpsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [domain]


    def parse(self, response):
        # scrape contact info
        for result in response.xpath('//*[@id="search-results-list"]/ul/li'):
            tempAddrArr = [i.strip() for i in result.xpath('a/span/text()').extract()]
            tempAddrArr = ", ".join(tempAddrArr)
            yield {
                'url': "https://www.jobs-ups.com" + result.xpath('a/@href').extract_first(),
                'title': result.xpath('a/h2/text()').extract_first(),
                'address': tempAddrArr,
            }
