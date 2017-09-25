import scrapy

class TargetedJobFairsSpider(scrapy.Spider):
    name = 'targetedjobfairs'
    allowed_domain = ["http://www.targetedjobfairs.com/"]
    start_urls = [ 'http://www.targetedjobfairs.com/' ]
    def parse(self, response):
        for result in response.css('tbody tr'):
            tmpUrl = result.xpath('td[4]/a/@href').extract_first()
            tmpUrl = response.urljoin(tmpUrl)
            yield response.follow(tmpUrl, self.parse_fair)
            '''
            yield {
                'date': result.css('td::text').extract_first(),
                'location': result.xpath('td[2]/text()').extract_first(),
                'title': result.xpath('td[3]/text()').extract_first(),
                'url': tmpUrl,
            }
            '''
            '''
            for href in response.xpath('//tbody/tr/td[4]/a/@href'):
                yield response.follow(href, self.parse_fair)
            '''

    def parse_mainpost(self, response):
        for sel in response.css('tbody tr div.pricing-table-wrap'):
            yield {
                'date': sel.css('td::text').extract_first(),
                'location': sel.xpath('td[2]/text()').extract_first(),
                'title': sel.xpath('td[3]/text()').extract_first(),
                'url': tmpUrl,
            }

    # scrape the page the link led me to
    def parse_fair(self, response):
        for sel in response.css('div.pricing-table-wrap'):
            yield {
                'event': sel.css('ul > li > div::text').extract_first(),
                #'date': sel.css('ul > li::text').extract_first(),
                #'hotel': sel.css('ul > li::text').extract()[2].strip(),
                #'address': sel.css('ul > li::text').extract()[3].strip(),
                #'api': sel.css('ul > li::text').extract(), #sel.css('ul > li[5] a::attr(href)').extract_first(),
            }
