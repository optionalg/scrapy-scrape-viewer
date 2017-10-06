import scrapy
from jobsups.items import JobsupsItem

import datetime

class JobsUpsSpider(scrapy.Spider):
    name = 'jobsups'
    allowed_domain = ["https://www.jobs-ups.com/"]
    #start_urls = [ 'https://www.jobs-ups.com/search-jobs/Florida' ]

    def __init__(self, domain='', *args,**kwargs):
        super(JobsUpsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [domain]

    def parse(self, response):
        # scrape for state list links
        for result in response.xpath('//*[@id="search-results-list"]/ul/li[3]'):


            upsurl = "https://www.jobs-ups.com" + result.xpath('a/@href').extract_first()
            yield response.follow(upsurl, self.parse_receiverTemplateJSON)

    # scrape the page the link led me to
    def parse_receiverTemplateJSON(self, response):
        # sender input data
        senderTemplateJSON = JobsupsItem()
        senderTemplateJSON['firstName'] = "Mezcel"
        senderTemplateJSON['middleName'] = " "
        senderTemplateJSON['lastName'] = "Matters"
        senderTemplateJSON['address'] = "123 Address Ln."
        senderTemplateJSON['city'] = "Sim City"
        senderTemplateJSON['state'] = "ST"
        senderTemplateJSON['zip'] = "12345"
        senderTemplateJSON['phone'] = "123-456-7890"
        senderTemplateJSON['email'] = "mezcel@mail.com"
        senderTemplateJSON['myUrl'] = "https://github.com/mezcel"

        # reciever input data
        for sel in response.xpath('//*[@id="content"]'):
            receiverTemplateJSON = JobsupsItem()
            environmentTemplateJSON = JobsupsItem()
            tempName = sel.css('#ajd-banner > section > div.ajd-job-title > div > div.ajd-job-button > a::attr(data-job-organization-id)').extract_first()
            receiverTemplateJSON['jobnameinputPrompt'] = "Job Post Name"
            receiverTemplateJSON['jobname'] = sel.css('#ajd-banner > section > div.ajd-job-title > div > div.ajd-job-heading > h1::text').extract_first()
            receiverTemplateJSON['jobidinputPrompt'] = "Job ID"
            receiverTemplateJSON['jobid'] = sel.css('#ajd-banner > section > div.ajd-job-title > div > div.ajd-job-button > a::attr(data-job-id)').extract_first()
            receiverTemplateJSON['hours'] = "1"
            receiverTemplateJSON['zip'] = "na"
            receiverTemplateJSON['website'] = response.request.url
            receiverTemplateJSON['attn'] = "UPS"
            receiverTemplateJSON['attnemail'] = "na"
            receiverTemplateJSON['phone'] = "na"
            receiverTemplateJSON['situation'] = "USP openings listed on www.jobs-ups.com"

            # environment input data
            environmentTemplateJSON['companyphilosophyinputPrompt'] = "Expecations"
            environmentTemplateJSON['companyphilosophy'] = sel.css('#anchor-overview > div > p::text').extract_first().strip()

            for sel1 in response.xpath('//*[@id="description"]'):
                # reciever input data
                receiverTemplateJSON['address'] = "Need To Find Addr"
                receiverTemplateJSON['city'] = sel1.xpath('//*[@id="description"]/div[1]/span[1]/text()').extract_first().strip()
                tempCity = sel1.xpath('//*[@id="description"]/div[1]/span[1]/text()').extract_first().strip()
                receiverTemplateJSON['state'] = sel1.xpath('//*[@id="description"]/div[1]/span[2]/text()').extract_first().strip()
                receiverTemplateJSON['name'] = "USP %s Store Id - %s"%(tempCity, tempName)

                # environment input data
                environmentTemplateJSON['companydescriptioninputPrompt'] = "Department Duty"
                environmentTemplateJSON['companydescription'] = sel.css('#description > div.ats-description::text').extract_first().strip()

            yield {
                'senderTemplateJSON': senderTemplateJSON,
                'receiverTemplateJSON': receiverTemplateJSON,
                'environmentTemplateJSON': environmentTemplateJSON,
                'relationshipTemplateJSON': {
                    "applicationidentityinputPrompt":"As a ...",
                    "applicationidentity": "front-end developer",
                    "skillarrayinputPrompt":"You are looking for talent who have skills in ...",
                    "skillarray": "C#, ASP.NET MVC, and Angular Java Script",
                    "knowledgearrayinputPrompt":"... , and I ...",
                    "knowledgearray": "have experience debugging, troubleshooting, and managing entity relationship databases on server and client side software. I am capable of being up-to-date with the latest developments in various technical fields",
                    "abilityarrayinputPrompt":"... , my abilities include ...",
                    "abilityarray": "solid theoretical foundations in various areas of computing, including algorithms & data structures, databases and especially distributed computing. I have experience appraising software requirements, management and applying database design"
                }
            }
