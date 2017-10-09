import scrapy
from jobsups.items import JobsupsItem

import datetime

class JobsUpsSpider(scrapy.Spider):
    name = 'jobsups'
    allowed_domain = ["https://www.jobs-ups.com/"]
    #start_urls = [ 'https://www.jobs-ups.com/search-jobs/Florida' ]

    count = 0

    def __init__(self, domain='', *args, **kwargs):
        super(JobsUpsSpider, self).__init__(*args, **kwargs)
        domain = domain.split(',')
        self.start_urls = domain

    def parse(self, response):
        # scrape for state list links
        for result in response.xpath('//*[@id="search-results-list"]/ul/li'):
            upsurl = "https://www.jobs-ups.com" + result.xpath('a/@href').extract_first()
            yield response.follow(upsurl, self.parse_receiverTemplateJSON)

    # render last stage of scrapy
    # the map and contacts page
    def parse_MapAddressPage(self, response):
        # count waypoint
        self.count = self.count + 1

        senderTemplateJSON = response.meta['senderTemplateJSON']
        receiverTemplateJSON = response.meta['receiverTemplateJSON']
        environmentTemplateJSON = response.meta['environmentTemplateJSON']

        # re-inputs address and contact based of formal location
        # it will overwrite the same information scraped from the previous page scrape
        for sel2 in response.css('#content'):
            # https://groups.google.com/forum/#!topic/scrapy-users/lX5lHQ1p9go
            addressString = sel2.css('div.content-container > section::attr(data-address)').extract_first().strip()
            addressArray = addressString.split(',')

            receiverTemplateJSON['address'] = addressArray[0]
            receiverTemplateJSON['city'] = addressArray[1]
            receiverTemplateJSON['state'] = addressArray[2]
            receiverTemplateJSON['zip'] = addressArray[3]

            yield {
                #json for scrapy-viewer
                'id': self.count,
                'url': receiverTemplateJSON['website'],
                'title': receiverTemplateJSON['jobname'],
                'address': addressString,
                'company': receiverTemplateJSON['name'],
                'date': datetime.datetime.now().strftime ("%Y%m%d"),
                # json for document-writer
                'senderTemplateJSON': senderTemplateJSON,
                'receiverTemplateJSON': receiverTemplateJSON,
                'environmentTemplateJSON': environmentTemplateJSON,
                'relationshipTemplateJSON': {
                    "applicationidentityinputPrompt":"As a ...",
                    "applicationidentity": "front-end developer",
                    "skillarrayinputPrompt":"You are looking for talent who have skills in ...",
                    "skillarray": "enter skills here",
                    "knowledgearrayinputPrompt":"... , and I ...",
                    "knowledgearray": "enter knowledge here",
                    "abilityarrayinputPrompt":"... , my abilities include ...",
                    "abilityarray": "enter ability here"
                },
                "emailletterTemplateJSON": {
                    "lead": receiverTemplateJSON['situation'],
                    "research":receiverTemplateJSON['website'],
                    "header":"A placeholder for a email header imported from a JSON file.",
                    "body":"<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p> <br> Dear <span class='highlighterDiv'>{{audience.attn}}</span>, <br><br> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I learned about, <span class='highlighterDiv'>{{audience.name}}</span>, through <span class='highlighterDiv'>{{leads.leadtype}}</span>. I am a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>. Based on what I learned from <span class='highlighterDiv'>{{leads.followup}}</span>, Department fullfillments <span class='highlighterDiv'>{{environmentsetting.companydescription}} needs to be filled by quified candidates.</span> Your target audience is geared toward <span class='highlighterDiv'>{{environmentsetting.companycustomers}}</span>. My interest in <span class = 'highlighterDiv' >{{desirability.skillarray}}</span> has inspired me to build upon what you started. <span class='highlighterDiv'>{{environmentsetting.companyphilosophy}}</span> <span class='highlighterDiv'>{{environmentsetting.companydistinguish}}</span> What you are doing is appealing. I would like to receive feedback or impressions regarding my eligability for <span class='highlighterDiv'>{{audience.jobname}}, {{audience.jobid}}</span>.</p>",
                    "footer":"A placeholder for a email footer imported from a JSON file."
                },
                "resumeTemplateJSON": {
                    "header":"<p align='center'><span class='highlighterDiv'>{{user.firstName}} {{user.middleName}} {{user.lastName}}<br>{{user.address}}, {{user.city}}, {{user.state}}, {{user.zip}}<br> {{user.phone}} {{user.email}}</span></p> <h3 align='center'>Resume</h3><hr> <p>I wish to contribute my labor and service to <span class='highlighterDiv'>{{audience.jobname}}</span>, {{audience.jobid}}</span>, for <span class='highlighterDiv'>{{audience.name}}</span>. Bellow is a keyword summary stating the knowledge, attitudes, and tastes I bring to the UPS culture and job site setting.</p>",
                    "body":"<p><b>Services</b></p><p><center><table><tr><td>keyword</td><td>keyword</td><td>keyword</td></tr><tr><td>keyword</td><td>keyword</td><td>keyword</td></tr><tr><td>keyword</td><td>keyword</td><td>keyword</td></tr></table></center></p>"
                },
                "coverletterTemplateJSON": {
                    "header": "<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p><p><span class='highlighterDiv'>{{audience.attn}}</span><br><span class='highlighterDiv'>{{audience.name}}</span><br><span class='highlighterDiv'>{{audience.zip}}</span></p><br>",
                    "body": "<p>Dear <span class='highlighterDiv'>{{audience.attn}}</span>,</p> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.middleName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I discovered <span class='highlighterDiv'>{{audience.situation}}</span>, at <span class='highlighterDiv'>{{audience.name}}</span>, and I want to contribute to your work. I consider myself skilled in <span class='highlighterDiv'>{{desirability.skillarray}}</span>. As a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>, <span class='highlighterDiv'>{{desirability.abilityarray}}</span>. I derive a personal satisfaction and pride when I fulfill the goals and expectations of <span class='highlighterDiv'>{{desirability.knowledgearray}}</span>. I am seeking to diversify my experience portfolio and further my way of life as a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>.</p><p class='tab'><span class='highlighterDiv'>{{audience.attn}}</span>, thank you for doing what you do, and thank you for taking the time to read how <span class='highlighterDiv'>{{audience.name}}</span> has inspired my own work.</p>",
                    "footer": "<br><p>Sincerely,</p><br><br> <p><span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.middleName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span><br><span class='highlighterDiv'>{{user.address}}</span>, <span class='highlighterDiv'>{{user.city}}</span>, <span class='highlighterDiv'>{{user.state}}</span>, <span class='highlighterDiv'>{{user.zip}}</span><br><span class='highlighterDiv'>{{user.email}}</span></p>"
                }
            }


    # scrape the start page linked me to
    # the bulk of the document-writer json will be written here
    # contains data about what job I will apply to
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

        # reciever input data as viewed from the main page
        for sel in response.xpath('//*[@id="content"]'):

            receiverTemplateJSON = JobsupsItem()
            environmentTemplateJSON = JobsupsItem()
            storeID = sel.css('#ajd-banner > section > div.ajd-job-title > div > div.ajd-job-button > a::attr(data-job-organization-id)').extract_first()

            receiverTemplateJSON['jobnameinputPrompt'] = "Job Post Name"
            receiverTemplateJSON['jobname'] = sel.css('#ajd-banner > section > div.ajd-job-title > div > div.ajd-job-heading > h1::text').extract_first()
            receiverTemplateJSON['jobidinputPrompt'] = "Job ID"
            receiverTemplateJSON['jobid'] = sel.css('#ajd-banner > section > div.ajd-job-title > div > div.ajd-job-button > a::attr(data-job-id)').extract_first()
            receiverTemplateJSON['hours'] = "1"
            receiverTemplateJSON['website'] = response.request.url
            receiverTemplateJSON['attn'] = "United Postal Service"
            receiverTemplateJSON['attnemail'] = sel.css('#ajd-banner > section > div.ajd-job-title > div > div.ajd-job-button > a::attr(href)').extract_first()
            receiverTemplateJSON['phone'] = "na"
            receiverTemplateJSON['situation'] = "openings listed on www.jobs-ups.com"

            # environment input data
            environmentTemplateJSON['companyphilosophyinputPrompt'] = "Expecations"
            environmentTemplateJSON['companyphilosophy'] = sel.css('#anchor-overview > div > p::text').extract_first().strip()

            for sel1 in response.xpath('//*[@id="description"]'):
                # reciever input data
                tempUrl = sel1.xpath('//*[@id="mapsection"]/span/a/@href').extract_first()
                tempUrl = "https://www.jobs-ups.com" + tempUrl

                # pre-contacts for reciever
                tempCity = sel1.xpath('//*[@id="description"]/div[1]/span[1]/text()').extract_first().strip()
                receiverTemplateJSON['city'] = "%s"%(tempCity)
                receiverTemplateJSON['state'] = sel1.xpath('//*[@id="description"]/div[1]/span[2]/text()').extract_first().strip()
                receiverTemplateJSON['name'] = "USP %s Store Id - %s"%(tempCity, storeID)

                # environment input data
                environmentTemplateJSON['companydescriptioninputPrompt'] = "Department Fullfilments"
                environmentTemplateJSON['companydescription'] = sel.css('#description > div.ats-description::text').extract_first().strip()

                yield scrapy.Request(tempUrl, self.parse_MapAddressPage, meta={'senderTemplateJSON':senderTemplateJSON, 'receiverTemplateJSON':receiverTemplateJSON, 'environmentTemplateJSON':environmentTemplateJSON})
