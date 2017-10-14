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
        emailletterTemplateJSON = JobsupsItem()
        resumeTemplateJSON = JobsupsItem()
        coverletterTemplateJSON = JobsupsItem()

        # count waypoint
        self.count = self.count + 1

        senderTemplateJSON = response.meta['senderTemplateJSON']
        receiverTemplateJSON = response.meta['receiverTemplateJSON']
        environmentTemplateJSON = response.meta['environmentTemplateJSON']
        relationshipTemplateJSON = response.meta['relationshipTemplateJSON']

        # re-inputs address and contact based of formal location
        # it will overwrite the same information scraped from the previous page scrape
        for sel2 in response.css('#content'):
            # https://groups.google.com/forum/#!topic/scrapy-users/lX5lHQ1p9go
            addressString = sel2.css('div.content-container > section::attr(data-address)').extract_first().strip()
            addressArray = addressString.split(',')

            # receiverTemplateJSON
            receiverTemplateJSON['address'] = addressArray[0]
            receiverTemplateJSON['city'] = addressArray[1]
            receiverTemplateJSON['state'] = addressArray[2]
            receiverTemplateJSON['zip'] = addressArray[3]

            # emailletterTemplateJSON
            emailletterTemplateJSON['lead'] = receiverTemplateJSON['situation']
            emailletterTemplateJSON['research'] = receiverTemplateJSON['website']
            emailletterTemplateJSON['header'] = "meznull"
            emailletterTemplateJSON['body'] = "meznull"
            emailletterTemplateJSON['footer'] = "meznull"

            # resumeTemplateJSON
            # coverletterTemplateJSON

            yield {
                #json for scrapy-viewer
                'id': self.count,
                'url': receiverTemplateJSON['website'],
                'title': receiverTemplateJSON['jobname'],
                'address': addressString,
                #'company': receiverTemplateJSON['name'],
                'company': addressString,
                'date': datetime.datetime.now().strftime ("%Y%m%d"),
                # json for document-writer
                'senderTemplateJSON': senderTemplateJSON,
                'receiverTemplateJSON': receiverTemplateJSON,
                'environmentTemplateJSON': environmentTemplateJSON,
                'relationshipTemplateJSON': relationshipTemplateJSON,
                "emailletterTemplateJSON": {
                    "lead": emailletterTemplateJSON['lead'],
                    "research": emailletterTemplateJSON['research'],
                    "header":"A placeholder for a email header imported from a JSON file.",
                    "body":"<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p> <br> Dear <span class='highlighterDiv'>{{audience.attn}}</span>, <br><br> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I learned about, <span class='highlighterDiv'>{{audience.name}}</span>, through <span class='highlighterDiv'>{{leads.leadtype}}</span>.  Based on what I learned from <span class='highlighterDiv'>{{leads.followup}}</span>, you are seeking the following. <span class='highlighterDiv'>{{environmentsetting.companydescription}}</span>. <span class='highlighterDiv'>{{environmentsetting.companycustomers}}</span>.  <span class = 'highlighterDiv' >{{desirability.skillarray}}</span>. <span class='highlighterDiv'>{{environmentsetting.companyphilosophy}}</span> <span class='highlighterDiv'>{{environmentsetting.companydistinguish}}</span>. This position and your company is appealing to me. I would like to receive feedback or impressions regarding my eligability for <span class='highlighterDiv'>{{audience.jobname}}, {{audience.jobid}}</span>.</p><br><p> Respectfully,</p> <span class = \"highlighterDiv\">{{user.firstName}}</span> <span class = \"highlighterDiv\"> {{user.middleName}} </span> <span class = \"highlighterDiv\">{{user.lastName}}</span> <br> <span class=\"highlighterDiv\">{{user.myUrl}}</span> <p></p>",
                    "footer":"A placeholder for a email footer imported from a JSON file."
                },
                "resumeTemplateJSON": {
                    "header":"<p align='center'><span class='highlighterDiv'>{{user.firstName}} {{user.middleName}} {{user.lastName}}<br>{{user.address}}, {{user.city}}, {{user.state}}, {{user.zip}}<br> {{user.phone}}, {{user.email}}</span></p> <h3 align='center'>Resume</h3><hr> <p>I am applying to <span class='highlighterDiv'>{{audience.jobname}}</span>, {{audience.jobid}}</span>, for <span class='highlighterDiv'>{{audience.name}}</span>. Bellow is a keyword summary of my application profile. I am flexable in regards to my available work hours, and I am flexible regarding travel and remote employment.</p>",
                    "body":"<p><b>Key Words</b></p><p><center><table><tr><td>Mechanic</td><td>Veteran (Honerable Discharge)</td><td>Drivers License </td></tr><tr><td>Secret Security Clearance (Expired)</td><td>U.S. Citizen</td><td>College Degree B.S.</td></tr><tr><td>No Allergies</td><td>No Fellonies</td><td>No Physical Limitations</td></tr></table></center></p><p><b>Education</b></p><p><u>Gannon University Erie, PA | B.S. Electrical/Computer Engineering, 2006</u><br>Electrical Engineering, Computer Engineering, Embedded SystemsPublished Scientific Journal on Artificial Intelligence</p><p></p><p><u>TCC, Tallahassee, FL | (Continued Education) Environmental Science, 2014</u><br>Environmental Systems, Plant Biology, Environmental Law/Regulations</p><p><u>Gannon University Erie, PA | (Masters Schooling) Information Analytics, 2015</u><br>Database Management, Requirements for Software Systems</p><p><b>Professional Experience</b></p><p><u>Independent Green Technologies (IGT) - Tallahassee, FL</u><br>CAD Specialist, 2014</p><p>My responsibility in the company focused on using computer aided design (CAD) tools to model price and cost projections for large-scale commercial organizations and residential stakeholders. The models were used to appraise and simulate design efficiency and feasibility to construct.</p><p><u>United States Coast Guard Cutter Mustang (WPB 1310) - Seward, AK</u><br>Machinery Technician, 2011-2013</p><p>As a member of a ship's engineering staff, I took the initiative to enhance our machinery related catalog and inventory database. Because of this initiative, enhancements were implemented service wide on that ship class. I used MS Access to develop a parts inventory catalog for EATON/Aeroquip brand high pressure hoses. This application was used to manage the preventative maintenance schedule, parts and pricing, and for ordering replacements for worn or damaged equipment and accessory parts.</p><p><u>Coast Guard Station Venice - Venice, LA</u><br>Search and Rescue, Boarding Officer, 2008-2011</p><p>In conjunction with search and rescue response duties, I developed a computer application to enhance safety and productivity. I used my computer technology skills to develop an HTML, CSS and RSS feed based application to gather weather, sea state and tidal information to assist in risk assessment for boats deploying in search and rescue operations.</p>"
                },
                "coverletterTemplateJSON": {
                    "header": "<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p><p><span class='highlighterDiv'>{{audience.attn}}</span><br><span class='highlighterDiv'>{{audience.name}}</span><br><span class='highlighterDiv'>{{audience.zip}}</span></p><br>",
                    "body": "<p>Dear <span class='highlighterDiv'>{{audience.attn}}</span>,</p> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.middleName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I learned about, <span class='highlighterDiv'>{{audience.name}}</span>, through <span class='highlighterDiv'>{{leads.leadtype}}</span>. <span class='highlighterDiv'>{{desirability.skillarray}}</span>. <span class='highlighterDiv'>{{desirability.abilityarray}}</span>. <span class='highlighterDiv'>{{desirability.knowledgearray}}</span>. I am seeking to diversify my experience portfolio and build professional relationships as a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>.</p><p class='tab'><span class='highlighterDiv'>{{audience.attn}}</span>, thank you for taking the time to consider my application. I hope to be of service to <span class='highlighterDiv'>{{audience.name}}</span>.</p>",
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
            relationshipTemplateJSON = JobsupsItem()
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
            receiverTemplateJSON['phone'] = "meznull"
            receiverTemplateJSON['situation'] = "openings listed on www.jobs-ups.com"

            # environment input data
            environmentTemplateJSON['companydescriptioninputPrompt'] = "You seek ..."
            environmentTemplateJSON['companydescription'] = sel.css('#anchor-overview > div > p::text').extract_first().strip()
            environmentTemplateJSON['companyphilosophyinputPrompt'] = "Attutude towards duties"
            environmentTemplateJSON['companyphilosophy'] = environmentTemplateJSON['companydescription']

            environmentTemplateJSON['companycustomersinputPrompt'] = "UPS Link: <a href='https://pressroom.ups.com/pressroom/ContentDetailsViewer.page?ConceptType=Speeches&id=1487961201475-136'>UPS Pressroom Abstract</a>"
            environmentTemplateJSON['companycustomers'] = "According to the UPS Pressroom Abstract, your customers picked up more than 36 million packages at Access Point locations, and the numbers continue to grow. Your UPS Mobile Returns of the more than 4,500 UPS Stores is expanding Saturday Ground services"
            environmentTemplateJSON['companydistinguishinputPrompt'] = "UPS Link: <a href='https://sustainability.ups.com/committed-to-more/'>committed-to-more</a>"
            environmentTemplateJSON['companydistinguish'] = " "

            # relationship input data
            relationshipTemplateJSON['applicationidentityinputPrompt'] = "Similar to Job Name"
            relationshipTemplateJSON['applicationidentity'] = receiverTemplateJSON['jobname']
            relationshipTemplateJSON['skillarrayinputPrompt'] = "My skills are, but not limited to ..."
            relationshipTemplateJSON['skillarray'] = environmentTemplateJSON['companydescription']
            relationshipTemplateJSON['knowledgearrayinputPrompt'] = "General Learning Refference"
            relationshipTemplateJSON['knowledgearray'] = "I received mechanics training though the Coast Guard and general literacy, logic, and reason though college."
            relationshipTemplateJSON['abilityarrayinputPrompt'] = "Abilities relevant to this post"
            relationshipTemplateJSON['abilityarray'] =  environmentTemplateJSON['companydescription']

            for sel1 in response.xpath('//*[@id="description"]'):
                # reciever input data
                tempUrl = sel1.xpath('//*[@id="mapsection"]/span/a/@href').extract_first()
                tempUrl = "https://www.jobs-ups.com" + tempUrl

                # pre-contacts for reciever
                tempCity = sel1.xpath('//*[@id="description"]/div[1]/span[1]/text()').extract_first().strip()
                receiverTemplateJSON['city'] = "%s"%(tempCity)
                receiverTemplateJSON['state'] = sel1.xpath('//*[@id="description"]/div[1]/span[2]/text()').extract_first().strip()
                receiverTemplateJSON['name'] = "USP %s Store id: %s"%(tempCity, storeID)

                # environment input data
                #environmentTemplateJSON['companydescriptioninputPrompt'] = "Department Fullfilments"
                #environmentTemplateJSON['companydescription'] = sel.css('#description > div.ats-description::text').extract_first().strip()

                yield scrapy.Request(tempUrl, self.parse_MapAddressPage, meta={'senderTemplateJSON':senderTemplateJSON, 'receiverTemplateJSON':receiverTemplateJSON, 'environmentTemplateJSON':environmentTemplateJSON, 'relationshipTemplateJSON':relationshipTemplateJSON})
