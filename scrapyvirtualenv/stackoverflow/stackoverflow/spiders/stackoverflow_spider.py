import scrapy

from stackoverflow.items import StackoverflowItem

# inspired by http://kimberlythegeek.com/scrape-stack-overflow-jobs/
# [Scrapy Tutorial](https://doc.scrapy.org/en/1.3/intro/tutorial.html)
class StackOverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domain = ["https://stackoverflow.com/"]
    # start_urls = [ 'https://stackoverflow.com/jobs?sort=p&l=Florida', 'https://stackoverflow.com/jobs?sort=p&l=Georgia', 'https://stackoverflow.com/jobs?sort=p&l=Alabama' ]

    count = 0

    def __init__(self, domain='', *args,**kwargs):
        super(StackOverflowSpider, self).__init__(*args, **kwargs)
        domain = domain.split(',')
        self.start_urls = domain

    def parse(self, response):
        emailletterTemplateJSON = StackoverflowItem()

        next_page = response.css('div.pagination > a.job-link::attr(href)').extract()
        mycounter = 0

        for result in response.css('div.main div.-job-summary'):
            joblink = result.css('a.job-link::attr(href)').extract_first()
            date = result.css('p.-posted-date.g-col::text').extract_first().strip()

            #if joblink:
            emailletterTemplateJSON['research'] = joblink

            emailletterTemplateJSON['lead'] = "Stackoverflow Jobs"
            emailletterTemplateJSON['date'] = date

            yield response.follow(joblink, self.parse_jobpost, meta={'emailletterTemplateJSON':emailletterTemplateJSON})

        #mycounter = mycounter + 1
        #yield scrapy.Request(response.urljoin(next_page[mycounter]), self.parse)

    def parse_jobpost(self, response):
        emailletterTemplateJSON = response.meta['emailletterTemplateJSON']
        receiverTemplateJSON = StackoverflowItem()
        environmentTemplateJSON = StackoverflowItem()
        relationshipTemplateJSON = StackoverflowItem()

        title = response.css('a.title::text').extract_first()
        if title:
            title = "title"
        titlejoblink = response.css('a.title::attr(href)').extract_first()
        if titlejoblink:
            titlejoblink = "titlejoblink"
        employer = response.css('a.employer::text').extract_first()
        if employer:
            employer = "employer"
        stackoverflowjobscompanies = response.css('a.employer::attr(href)').extract_first()
        if stackoverflowjobscompanies:
            stackoverflowjobscompanies = "stackoverflowjobscompanies"
        location = response.css('div.-description > div:nth-child(2) > div:nth-child(2)::text').extract_first()
        if location:
            location = "location"

        email = response.css('a.mail::attr(href)').extract_first()
        if email:
            email = "email"

        for aboutthisjob in response.css('.-about-job'):
            jobtype = aboutthisjob.css('.-about-job-items > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)::text').extract_first()
            if not jobtype:
                jobtype = "job type"
            experiencelevel = aboutthisjob.css('.-about-job-items > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').extract_first()
            if not experiencelevel:
                experiencelevel = "experience level"
            role = aboutthisjob.css('.-about-job-items > div:nth-child(1) > div:nth-child(3) > span:nth-child(2)::text').extract_first()
            if not role:
                role = "role"
            industry = aboutthisjob.css('div.g-column:nth-child(2) > div:nth-child(1) > span:nth-child(2)::text').extract_first()
            if not industry:
                industry = "industry"
            companysize = aboutthisjob.css('div.g-column:nth-child(2) > div:nth-child(2) > span:nth-child(2)::text').extract_first()
            if not companysize:
                companysize = "company size"
            companytype = aboutthisjob.css('div.g-column:nth-child(2) > div:nth-child(3) > span:nth-child(2)::text').extract_first()
            if not companytype:
                companytype = "company type"

        for technologies in response.css('.-technologies'):
            technology = technologies.css('div.-tags:nth-child(2) > p:nth-child(1) > a::text').extract()
            technology = ", ".join(technology)

        for jobdescription in response.css('.-job-description'):
            descriptionBlob = jobdescription.css('.-job-description > div.description').extract_first().replace('\r\n', '').strip()
            descriptionBlob = descriptionBlob.replace('<div class="description">', '').strip()
            descriptionBlob = descriptionBlob.replace('</div>', '').strip()

        receiverTemplateJSON['jobnameinputPrompt'] = "Position:"
        receiverTemplateJSON['jobname'] = title
        receiverTemplateJSON['jobidinputPrompt'] = "Job Type:"
        receiverTemplateJSON['jobid'] = role
        receiverTemplateJSON['hours'] = jobtype
        receiverTemplateJSON['name'] = employer
        receiverTemplateJSON['address'] =  " "

        # citystate = location.split(',')
        # receiverTemplateJSON['city'] =  citystate[0]
        # receiverTemplateJSON['state'] =  citystate[1]
        receiverTemplateJSON['city'] =  ' '
        receiverTemplateJSON['state'] =  ' '

        receiverTemplateJSON['zip'] =  " "
        receiverTemplateJSON['website'] = stackoverflowjobscompanies
        receiverTemplateJSON['attn'] = ""
        receiverTemplateJSON['attnemail'] = email
        receiverTemplateJSON['phone'] = ""
        receiverTemplateJSON['situation'] = emailletterTemplateJSON['lead']

        environmentTemplateJSON['companydescriptioninputPrompt'] = "<a href='https://stackoverflow.com" + titlejoblink + "' target='_blank'>Link: Stackoverflow Companies</a>"
        environmentTemplateJSON['companydescription'] = descriptionBlob
        environmentTemplateJSON['companyphilosophyinputPrompt'] = ""
        environmentTemplateJSON['companyphilosophy'] = companytype
        environmentTemplateJSON['companycustomersinputPrompt'] = ""
        environmentTemplateJSON['companycustomers'] = industry
        environmentTemplateJSON['companydistinguishinputPrompt'] = ""
        environmentTemplateJSON['companydistinguish'] = companysize

        relationshipTemplateJSON['applicationidentityinputPrompt'] = ""
        relationshipTemplateJSON['applicationidentity'] = role
        relationshipTemplateJSON['skillarrayinputPrompt'] = ""
        relationshipTemplateJSON['skillarray'] = technology
        relationshipTemplateJSON['knowledgearrayinputPrompt'] = ""
        relationshipTemplateJSON['knowledgearray'] = technology
        relationshipTemplateJSON['abilityarrayinputPrompt'] = ""
        relationshipTemplateJSON['abilityarray'] = technology

        emailletterTemplateJSON['research'] = titlejoblink

        yield response.follow(stackoverflowjobscompanies, self.parse_stackoverflowjobscompanies, meta={'emailletterTemplateJSON':emailletterTemplateJSON, 'receiverTemplateJSON':receiverTemplateJSON, 'environmentTemplateJSON':environmentTemplateJSON, 'relationshipTemplateJSON':relationshipTemplateJSON})

    # https://stackoverflow.com/jobs/companies/
    def parse_stackoverflowjobscompanies(self, response):
        emailletterTemplateJSON = response.meta['emailletterTemplateJSON']
        receiverTemplateJSON = response.meta['receiverTemplateJSON']
        environmentTemplateJSON = response.meta['environmentTemplateJSON']
        relationshipTemplateJSON = response.meta['relationshipTemplateJSON']

        companyhomepage = response.css('#company-profile > div:nth-child(2) > div.right > div:nth-child(1) > a:nth-child(1)::attr(href)').extract_first()

        address = response.css('.address::text').extract()
        #if address:
        receiverTemplateJSON['address'] = address
        receiverTemplateJSON['zip'] = address

        receiverTemplateJSON['website'] = companyhomepage

        self.count = self.count + 1

        yield {
            'id': self.count,
            'job': receiverTemplateJSON['jobname'],
            'title': receiverTemplateJSON['jobid'],
            'url': emailletterTemplateJSON['research'],
            'company': receiverTemplateJSON['name'],
            'location': receiverTemplateJSON['address'],
            #'date': emailletterTemplateJSON['date'],
            'date': emailletterTemplateJSON['research'],
            'skills': relationshipTemplateJSON['skillarray'],
            'receiverTemplateJSON':receiverTemplateJSON,
            'environmentTemplateJSON':environmentTemplateJSON,
            'relationshipTemplateJSON':relationshipTemplateJSON,
            'emailletterTemplateJSON':emailletterTemplateJSON

        }
