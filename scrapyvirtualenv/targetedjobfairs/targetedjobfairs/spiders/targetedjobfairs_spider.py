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
        # //*[@id="main"]/div/div/main/div/div/div[2]
        #for sel in response.css('div.pricing-table-wrap'):
        for sel in response.xpath('//*[@id="main"]/div/div/main/div/div/div[2]'):
            # strip and concat my address array
            tempAddrArr = [i.strip() for i in sel.xpath('div[1]/div/ul/li[5]/text()').extract()]
            tempAddrArr = ", ".join(tempAddrArr)
            yield {
                'event': sel.xpath('div[1]/div/ul/li[1]/div/text()').extract_first(), #//*[@id="main"]/div/div/main/div/div/div[2]/div[1]/div/ul/li[1]/div
                'date': sel.xpath('div[1]/div/ul/li[2]/text()').extract_first(), #//*[@id="main"]/div/div/main/div/div/div[2]/div[1]/div/ul/li[2]
                'hotel': sel.xpath('div[1]/div/ul/li[4]/text()').extract_first(), #//*[@id="main"]/div/div/main/div/div/div[2]/div[1]/div/ul/li[4]
                'address': tempAddrArr,
                #[i.strip() for i in sel.xpath('div[1]/div/ul/li[5]/text()').extract()], # //*[@id="main"]/div/div/main/div/div/div[2]/div[1]/div/ul/li[5]
                # [i.strip() for i in id.select('text()').extract()]
                # 'address': sel.xpath('div[1]/div/ul/li[5]/text()').extract()[0].strip()
                'participants': sel.xpath('div[2]/div/ul/li/text()').extract(), #//*[@id="main"]/div/div/main/div/div/div[2]/div[2]/div/ul/li[2]
                #//*[@id="main"]/div/div/main/div/div/div[2]/div[2]/div/ul/li[13]
            }
