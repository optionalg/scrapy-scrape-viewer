import scrapy

from stackoverflow.items import StackoverflowItem


# inspired by http://kimberlythegeek.com/scrape-stack-overflow-jobs/
# [Scrapy Tutorial](https://doc.scrapy.org/en/1.3/intro/tutorial.html)
class StackOverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domain = ["https://stackoverflow.com/"]
    # start_urls = [ 'https://stackoverflow.com/jobs?sort=p&l=Florida', 'https://stackoverflow.com/jobs?sort=p&l=Georgia', 'https://stackoverflow.com/jobs?sort=p&l=Alabama' ]

    def __init__(self, domain='', *args,**kwargs):
        super(StackOverflowSpider, self).__init__(*args, **kwargs)
        domain = domain.split(',')
        self.start_urls = domain

    def parse(self, response):
        receiverTemplateJSON = StackoverflowItem()
        relationshipTemplateJSON = StackoverflowItem()

        for result in response.css('div.main div.-job-summary'):
            receiverTemplateJSON['jobnameinputPrompt'] = "Position:"
            receiverTemplateJSON['jobname'] = result.css('a.job-link::text').extract_first()
            receiverTemplateJSON['jobidinputPrompt'] = "Job Type:"
            receiverTemplateJSON['jobid'] = result.css('a.job-link::attr(title)').extract_first()
            receiverTemplateJSON['hours'] = "1"
            receiverTemplateJSON['name'] = result.css('a.job-link::attr(title)').extract_first()
            receiverTemplateJSON['address'] =  result.css('div.-location::text').extract_first().replace('- \r\n', '').strip()
            receiverTemplateJSON['city'] =  result.css('div.-location::text').extract_first().replace('- \r\n', '').strip()
            receiverTemplateJSON['state'] =  result.css('div.-location::text').extract_first().replace('- \r\n', '').strip()
            receiverTemplateJSON['zip'] =  result.css('div.-location::text').extract_first().replace('- \r\n', '').strip()
            receiverTemplateJSON['website'] = result.css('a.job-link::attr(href)').extract_first()
            receiverTemplateJSON['attn'] = "meznull"
            receiverTemplateJSON['attnemail'] = "meznull"
            receiverTemplateJSON['phone'] = "meznull"
            receiverTemplateJSON['situation'] = "Stack Overflow Jobs Pros Online"


            relationshipTemplateJSON['skillarray'] = result.css('p > a.post-tag.job-link.no-tag-menu::text').extract()

            yield response.follow(receiverTemplateJSON['website'], self.parse_jobpost, meta={'receiverTemplateJSON':receiverTemplateJSON, 'relationshipTemplateJSON':relationshipTemplateJSON })


            '''
            yield {
                'job': result.css('a.job-link::text').extract_first(),
                'title': result.css('a.job-link::attr(title)').extract_first(),
                'url': result.css('a.job-link::attr(href)').extract_first(),
                'company': result.css('div.-name::text').extract_first().strip(),
                'location': result.css('div.-location::text').extract_first().replace('- \r\n', '').strip(),
                'date': result.css('p.-posted-date.g-col::text').extract_first().strip(),
                'skills': result.css('p > a.post-tag.job-link.no-tag-menu::text').extract()
            }
            '''

            next_page = response.css('div.pagination > a.job-link::attr(href)').extract()
            mycounter = 1
            if next_page[mycounter + 1]:
                mycounter = mycounter + 1
                next_page = response.urljoin(next_page[mycounter])
                yield scrapy.Request(next_page, self.parse)


    def parse_jobpost(self, response):
        receiverTemplateJSON = response.meta['receiverTemplateJSON']
        relationshipTemplateJSON = response.meta['relationshipTemplateJSON']

        environmentTemplateJSON = StackoverflowItem()

        # for result2 in response.css('.-about-job'):
        for result3 in response.css('.-technologies'):
        # for result4 in response.css('.-job-description'):


            environmentTemplateJSON['companydescriptioninputPrompt'] = ""
            environmentTemplateJSON['companydescription'] = ""
            environmentTemplateJSON['companyphilosophyinputPrompt'] = ""
            environmentTemplateJSON['companyphilosophy'] = ""
            environmentTemplateJSON['companycustomersinputPrompt'] = ""
            environmentTemplateJSON['companycustomers'] = ""
            environmentTemplateJSON['companydistinguishinputPrompt'] = ""
            environmentTemplateJSON['companydistinguish'] = ""

            relationshipTemplateJSON['applicationidentityinputPrompt'] = ""
            relationshipTemplateJSON['applicationidentity'] = ""
            relationshipTemplateJSON['skillarrayinputPrompt'] = ""
            #relationshipTemplateJSON['skillarray'] = ""
            relationshipTemplateJSON['knowledgearrayinputPrompt'] = ""
            relationshipTemplateJSON['knowledgearray'] = result3.css('div.-tags:nth-child(2) > p:nth-child(1) > a:nth-child(1)::text').extract_first()
            relationshipTemplateJSON['abilityarrayinputPrompt'] = ""
            relationshipTemplateJSON['abilityarray'] = ""

            yield {
                'job': receiverTemplateJSON['jobname'],
                'title': receiverTemplateJSON['jobid'],
                'url': receiverTemplateJSON['website'],
                'company': receiverTemplateJSON['jobid'],
                'location': receiverTemplateJSON['address'],
                'date': "date",
                'skills': relationshipTemplateJSON['skillarray'],
                'receiverTemplateJSON': receiverTemplateJSON,
                'relationshipTemplateJSON': relationshipTemplateJSON,
                'environmentTemplateJSON': environmentTemplateJSON,
            }
