import scrapy
import datetime

class JobsUpsSpider(scrapy.Spider):
    name = 'jobsups'
    allowed_domain = ["hhttps://www.jobs-ups.com/"]
    #start_urls = [ 'https://www.jobs-ups.com/search-jobs/Florida' ]

    def __init__(self, domain='', *args,**kwargs):
        super(JobsUpsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [domain]


    def parse(self, response):
        # scrape contact info
        for result in response.xpath('//*[@id="search-results-list"]/ul/li'):
            # tempAddrArr = [i.strip() for i in result.xpath('a/span/text()').extract()]
            # tempAddrArr = ", ".join(tempAddrArr)
            tempAddrArr = result.xpath('a/span[2]/text()').extract()
            tempAddrArr = tempAddrArr + result.xpath('a/span[3]/text()').extract()
            tempAddrArr = ", ".join(tempAddrArr)
            yield {
                'url': "https://www.jobs-ups.com" + result.xpath('a/@href').extract_first(),
                'title': result.xpath('a/h2/text()').extract_first(),
                'address': "UPS, " + tempAddrArr,
                'company': result.xpath('a/span[1]/text()').extract_first(),
                'date': datetime.datetime.now().strftime ("%Y%m%d"),
            }
            # follow pagination links
            next_page = response.xpath('//*[@id="pagination-bottom"]/div[2]/a[2]/@href').extract_first()
            if next_page is not None:
                next_page = "https://www.jobs-ups.com" + next_page
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
