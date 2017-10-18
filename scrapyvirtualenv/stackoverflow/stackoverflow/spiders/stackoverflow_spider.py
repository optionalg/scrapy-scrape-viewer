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
        receiverTemplateJSON = StackoverflowItem()
        relationshipTemplateJSON = StackoverflowItem()
        item = StackoverflowItem()

        mycounter = 0
        for result in response.css('div.main div.-job-summary'):
            receiverTemplateJSON['jobnameinputPrompt'] = "Position:"
            receiverTemplateJSON['jobname'] = result.css('a.job-link::text').extract_first()
            receiverTemplateJSON['jobidinputPrompt'] = "Job Type:"
            receiverTemplateJSON['jobid'] = result.css('a.job-link::attr(title)').extract_first()
            receiverTemplateJSON['hours'] = "1"
            receiverTemplateJSON['name'] = result.css('a.job-link::attr(title)').extract_first()
            receiverTemplateJSON['address'] =  " "

            citystate = result.css('div.-location::text').extract_first().replace('- \r\n', '').strip()
            citystate = citystate.split(', ')
            receiverTemplateJSON['city'] =  citystate[0]
            receiverTemplateJSON['state'] =  citystate[1]

            receiverTemplateJSON['zip'] =  " "

            nextlistlink = result.css('a.job-link::attr(href)').extract_first()
            receiverTemplateJSON['website'] = nextlistlink
            receiverTemplateJSON['attn'] = ""
            receiverTemplateJSON['attnemail'] = ""
            receiverTemplateJSON['phone'] = ""
            receiverTemplateJSON['situation'] = "Stack Overflow Jobs"

            relationshipTemplateJSON['skillarray'] = result.css('p > a.post-tag.job-link.no-tag-menu::text').extract()

            item['date'] = result.css('p.-posted-date.g-col::text').extract_first().strip()
            item['website'] = receiverTemplateJSON['website']

            yield response.follow(nextlistlink, self.parse_jobpost, meta={'receiverTemplateJSON':receiverTemplateJSON, 'relationshipTemplateJSON':relationshipTemplateJSON, 'item':item })

        '''next_page = response.css('div.pagination > a.job-link::attr(href)').extract()
        mycounter = mycounter + 1
        yield scrapy.Request(response.urljoin(next_page[mycounter]), self.parse)'''


    def parse_jobpost(self, response):
        receiverTemplateJSON = response.meta['receiverTemplateJSON']
        relationshipTemplateJSON = response.meta['relationshipTemplateJSON']
        item = response.meta['item']
        environmentTemplateJSON = StackoverflowItem()
        emailletterTemplateJSON = StackoverflowItem()

        employer = response.css('a.employer::text').extract_first()
        employerLink = response.css('a.employer::attr(href)').extract_first()
        employerLink = "https://stackoverflow.com" + employerLink

        receiverTemplateJSON['name'] = employer
        emailletterTemplateJSON['lead'] = "Stack Overflow Jobs"
        emailletterTemplateJSON['research'] = receiverTemplateJSON['website']
        receiverTemplateJSON['website'] = employerLink

        for result2 in response.css('.-about-job'):
            jobtype = result2.css('.-about-job-items > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)::text').extract_first()
            experiencelevel = result2.css('.-about-job-items > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').extract_first()
            role = result2.css('.-about-job-items > div:nth-child(1) > div:nth-child(3) > span:nth-child(2)::text').extract_first()
            industry = result2.css('div.g-column:nth-child(2) > div:nth-child(1) > span:nth-child(2)::text').extract_first()
            companysize = result2.css('div.g-column:nth-child(2) > div:nth-child(2) > span:nth-child(2)::text').extract_first()
            companytype = result2.css('div.g-column:nth-child(2) > div:nth-child(3) > span:nth-child(2)::text').extract_first()

        receiverTemplateJSON['jobid'] = experiencelevel
        receiverTemplateJSON['hours'] = jobtype

        for result3 in response.css('.-technologies'):
            technology = result3.css('div.-tags:nth-child(2) > p:nth-child(1) > a::text').extract()

        technology = ", ".join(technology)

        for result4 in response.css('.-job-description'):
            description = result4.css('.-job-description > div.description').extract_first().replace('\r\n', '').strip()
            description = description.replace('<div class="description">', '').strip()
            description = description.replace('</div>', '').strip()

        environmentTemplateJSON['companydescriptioninputPrompt'] = "<a href='"+employerLink+"' target='_blank'>Link: Stackoverflow Companies</a>"
        environmentTemplateJSON['companydescription'] = description
        environmentTemplateJSON['companyphilosophyinputPrompt'] = ""
        environmentTemplateJSON['companyphilosophy'] = description
        environmentTemplateJSON['companycustomersinputPrompt'] = ""
        environmentTemplateJSON['companycustomers'] = companytype + ", "+ industry
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

        emailletterTemplateJSON['lead'] = "Stack Overflow Jobs"
        emailletterTemplateJSON['research'] = receiverTemplateJSON['website']

        yield response.follow(employerLink, self.parse_googleApiPage, meta={'receiverTemplateJSON':receiverTemplateJSON, 'relationshipTemplateJSON':relationshipTemplateJSON, 'item':item, 'environmentTemplateJSON':environmentTemplateJSON, 'emailletterTemplateJSON':emailletterTemplateJSON })


    def parse_googleApiPage(self, response):
        receiverTemplateJSON = response.meta['receiverTemplateJSON']
        relationshipTemplateJSON = response.meta['relationshipTemplateJSON']
        environmentTemplateJSON = response.meta['environmentTemplateJSON']
        emailletterTemplateJSON = response.meta['emailletterTemplateJSON']
        item = response.meta['item']

        companyhomepage = response.css('#company-profile > div:nth-child(2) > div.right > div:nth-child(1) > a:nth-child(1)::attr(href)').extract_first()
        receiverTemplateJSON['website'] = companyhomepage

        finaladdress = response.xpath('//*[@id="company-profile"]/div[8]/div[1]/div[1]/text()').extract_first()
        if (finaladdress):
            receiverTemplateJSON['address'] = googleapiaddress
            receiverTemplateJSON['zip'] = googleapiaddress

        self.count = self.count + 1

        yield {
            'id': self.count,
            'job': receiverTemplateJSON['jobname'],
            'title': receiverTemplateJSON['jobname'] +", " + receiverTemplateJSON['jobid'],
            'url': item['website'],
            'company': receiverTemplateJSON['name'] + ", " +receiverTemplateJSON['city'] + ", "+ receiverTemplateJSON['state'],
            'location': receiverTemplateJSON['city'] + ", "+ receiverTemplateJSON['state'],
            'date': item['date'],
            'skills': relationshipTemplateJSON['skillarray'],

            'receiverTemplateJSON': receiverTemplateJSON,
            'relationshipTemplateJSON': relationshipTemplateJSON,
            'environmentTemplateJSON': environmentTemplateJSON,
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
