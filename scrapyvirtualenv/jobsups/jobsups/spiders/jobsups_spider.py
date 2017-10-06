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
                },
                "emailletterTemplateJSON": {
                    "lead":"a Google search for Stations of the Cross art",
                    "research":"your blog site",
                    "header":"A placeholder for a email header imported from a JSON file.",
                    "body":"<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p> <br> Dear <span class='highlighterDiv'>{{audience.attn}}</span>, <br><br> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I learned about, <span class='highlighterDiv'>{{audience.name}}</span>, through <span class='highlighterDiv'>{{leads.leadtype}}</span>. I am a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>. Based on what I learned from <span class='highlighterDiv'>{{leads.followup}}</span>, I see that <span class='highlighterDiv'>{{environmentsetting.companydescription}}</span> Your target audience is geared toward <span class='highlighterDiv'>{{environmentsetting.companycustomers}}</span>. My interest in <span class = 'highlighterDiv' >{{desirability.skillarray}}</span> has inspired me to build upon what you started. <span class='highlighterDiv'>{{environmentsetting.companyphilosophy}}</span> <span class='highlighterDiv'>{{environmentsetting.companydistinguish}}</span> What you are doing is appealing. I would like to receive feedback or impressions regarding the appeal of <span class='highlighterDiv'>{{audience.jobid}}</span>.</p>",
                    "footer":"A placeholder for a email footer imported from a JSON file."
                },
                "resumeTemplateJSON": {
                    "header":"<p align='center'><span class='highlighterDiv'>{{user.firstName}} {{user.middleName}} {{user.lastName}}<br>{{user.address}}, {{user.city}}, {{user.state}}, {{user.zip}}<br> {{user.phone}} {{user.email}}</span></p> <h3 align='center'>Resume</h3><hr> <p>I wish to share my potential contribution to your <span class='highlighterDiv'>{{audience.jobname}}</span>, specifically through <span class='highlighterDiv'>{{audience.jobid}}</span>, for <span class='highlighterDiv'>{{audience.name}}</span>. Bellow is a keyword summary stating the knowledge set which forged my personality and perspective as a developer.</p>",
                    "body":"<p><b>Services</b></p><p><center><table><tr><td>Embedded System Analysis</td><td>Debugging &amp; Troubleshooting</td><td>Testing &amp; Documentation</td></tr><tr><td>Software Development</td><td>Requirements Management</td><td>Project Management</td></tr><tr><td>Coding &amp; Scripting</td><td>GUI Design</td><td>Database Design</td></tr></table></center></p><p><b>Technology Summary</b></p><p><u>Programming</u>: C, C ++, C#, XML, CSV, SVG, MySQL, MSSql, HTML, VB.Net, ASP.NET, ADO.NET, LINQ, Java, JavaScript, AngularJS, jQuery, CSS, and PHP</p><p><u>Development Tools</u>: MS Visual Studio 2012, MS Sql Server Management Studio, MySql Workbench, WAMP Server, Oracle NetBeans IDE, Notepad ++, Inkscape and Sketchup (CAD), MS Office Suite</p><p><u>Systems</u>: Windows, Dot NET</p>",
                    "footer":"A placeholder for a resume footer imported from a JSON file."
                },
                "coverletterTemplateJSON": {
                    "header": "<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p><p><span class='highlighterDiv'>{{audience.attn}}</span><br><span class='highlighterDiv'>{{audience.name}}</span><br><span class='highlighterDiv'>{{audience.zip}}</span></p><br>",
                    "body": "<p>Dear <span class='highlighterDiv'>{{audience.attn}}</span>,</p> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.middleName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I discovered <span class='highlighterDiv'>{{audience.situation}}</span>, at <span class='highlighterDiv'>{{audience.name}}</span>, and I want to contribute to your work. I consider myself skilled in <span class='highlighterDiv'>{{desirability.skillarray}}</span>. As a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>, <span class='highlighterDiv'>{{desirability.abilityarray}}</span>. I derive a personal satisfaction and pride when I fulfill the goals and expectations of <span class='highlighterDiv'>{{desirability.knowledgearray}}</span>. I am seeking to diversify my experience portfolio and further my way of life as a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>.</p><p class='tab'><span class='highlighterDiv'>{{audience.attn}}</span>, thank you for doing what you do, and thank you for taking the time to read how <span class='highlighterDiv'>{{audience.name}}</span> has inspired my own work.</p>",
                    "footer": "<br><p>Sincerely,</p><br><br> <p><span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.middleName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span><br><span class='highlighterDiv'>{{user.address}}</span>, <span class='highlighterDiv'>{{user.city}}</span>, <span class='highlighterDiv'>{{user.state}}</span>, <span class='highlighterDiv'>{{user.zip}}</span><br><span class='highlighterDiv'>{{user.email}}</span></p>"
                }
            }
