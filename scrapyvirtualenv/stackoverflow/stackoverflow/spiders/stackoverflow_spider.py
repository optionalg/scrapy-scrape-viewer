import scrapy
import re

from stackoverflow.items import StackoverflowItem

# stackoverflow_spider.py WIP file
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
        for result in response.css('div.main div.-job-summary'):
            nextlistlink = result.css('a.job-link::attr(href)').extract_first()
            yield response.follow(nextlistlink, self.parse_jobpost)

    def parse_jobpost(self, response):
        parse_jobpost_receiverTemplateJSON = StackoverflowItem()
        parse_jobpost_environmentTemplateJSON = StackoverflowItem()
        parse_jobpost_relationshipTemplateJSON = StackoverflowItem()
        parse_jobpost_emailletterTemplateJSON = StackoverflowItem()

        for jobdetaildescription in response.css('#job-detail > div.job-detail-header > div > div.-description'):
            title = jobdetaildescription.css('div:nth-child(1) > h1 > a::text').extract_first()
            # title link is = response.request.url
            employer = jobdetaildescription.css('div.-company.g-row > div.-name > a::text').extract_first()
            employerLink = "https://stackoverflow.com" + response.css('a.employer::attr(href)').extract_first()
            location = jobdetaildescription.css('div.-company.g-row > div.-location::text').extract_first()

        for aboutthisjob in response.css('.-about-job'):
            jobtype = aboutthisjob.css('.-about-job-items > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)::text').extract_first()
            experiencelevel = aboutthisjob.css('.-about-job-items > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').extract_first()

        for jobdescription in response.css('.-job-description'):
            description = jobdescription.css('.-job-description > div.description').extract_first()

        mailtolink = response.css('#action-bar > div.g-row.-share-report > div:nth-child(1) > a::attr(href)').extract_first()

        # ### receiverTemplateJSON ##################################
        parse_jobpost_receiverTemplateJSON['jobname'] = title
        parse_jobpost_receiverTemplateJSON['name'] = employer
        parse_jobpost_receiverTemplateJSON['jobid'] = experiencelevel
        parse_jobpost_receiverTemplateJSON['hours'] = jobtype
        parse_jobpost_receiverTemplateJSON['attnemail'] = "https://stackoverflow.com" + mailtolink
        parse_jobpost_receiverTemplateJSON['state'] = location

        # ### environmentTemplateJSON ##################################
        parse_jobpost_environmentTemplateJSON['companydescriptioninputPrompt'] = "<a href='" + response.request.url + "' target='_blank'>Link: Stackoverflow Job Detail</a>"
        parse_jobpost_environmentTemplateJSON['companydescription'] = description

        # ### relationshipTemplateJSO ##################################
        parse_jobpost_relationshipTemplateJSON['applicationidentityinputPrompt'] = ""
        parse_jobpost_relationshipTemplateJSON['applicationidentity'] = title
        parse_jobpost_relationshipTemplateJSON['abilityarrayinputPrompt'] = ""
        parse_jobpost_relationshipTemplateJSON['abilityarray'] = experiencelevel

        # ### emailletterTemplateJSON ##################################
        parse_jobpost_emailletterTemplateJSON['research'] = response.request.url


        yield response.follow(employerLink, self.parse_googleApiPage, meta={'parse_jobpost_receiverTemplateJSON':parse_jobpost_receiverTemplateJSON, 'parse_jobpost_environmentTemplateJSON':parse_jobpost_environmentTemplateJSON, 'parse_jobpost_relationshipTemplateJSON':parse_jobpost_relationshipTemplateJSON, 'parse_jobpost_emailletterTemplateJSON':parse_jobpost_emailletterTemplateJSON})

    def parse_googleApiPage(self, response):
        parse_jobpost_receiverTemplateJSON = response.meta['parse_jobpost_receiverTemplateJSON']
        parse_jobpost_environmentTemplateJSON = response.meta['parse_jobpost_environmentTemplateJSON']
        parse_jobpost_relationshipTemplateJSON = response.meta['parse_jobpost_relationshipTemplateJSON']
        parse_jobpost_emailletterTemplateJSON = response.meta['parse_jobpost_emailletterTemplateJSON']

        items = StackoverflowItem()
        receiverTemplateJSON = StackoverflowItem()
        relationshipTemplateJSON = StackoverflowItem()
        environmentTemplateJSON = StackoverflowItem()
        emailletterTemplateJSON = StackoverflowItem()

        # #################################### #

        industry = response.css('#company-profile > div:nth-child(2) > ul > li:nth-child(3) > span::text').extract_first()
        companysize = response.css('#company-profile > div:nth-child(2) > ul > li:nth-child(2) > span::text').extract_first()
        companytype = response.css('#company-profile > div:nth-child(2) > ul > li:nth-child(1) > span::text').extract_first()
        companyname = response.css('.title-and-badge > h1:nth-child(1)::text').extract_first()
        companyphil = response.css('.first-company-statement').extract()
        if not companyphil:
            companyphil = "no extra data on Stackoverflow"
        companyhomepage = response.css('#company-profile > div:nth-child(2) > div.right > div:nth-child(1) > a:nth-child(1)::attr(href)').extract_first()

        for techenvironment in response.css('div.tags'):
            skills = techenvironment.css('a::text').extract()

        skills = ", ".join(skills)

        finaladdress = ""

        if not response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[1]').extract_first():
            finaladdress = parse_jobpost_receiverTemplateJSON['state']


        if response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[1]').extract_first():
            finaladdress1 = response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[1]').extract_first()
            #finaladdress = finaladdress1

            if (finaladdress1 == "USA"):
                finaladdress = parse_jobpost_receiverTemplateJSON['state']

            if response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[2]').extract_first():
                finaladdress2 = response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[2]').extract_first()
                finaladdress = finaladdress1 + " " + finaladdress2

                if response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[3]').extract_first():
                    finaladdress3 = response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[3]').extract_first()
                    finaladdress = finaladdress1 + " " + finaladdress2 + " " + finaladdress3

                    if response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[4]').extract_first():
                        finaladdress4 = response.xpath('//*[@id="company-profile"]/div[9]/div[1]/div[1]/text()[4]').extract_first()
                        finaladdress = finaladdress1 + " " + finaladdress2 + " " + finaladdress3 + " " + finaladdress4


            if finaladdress:
                finaladdress = re.sub('\s+',' ',finaladdress)

        # ### items #################################### #
        items['id'] = self.count
        items['job'] = companyname
        items['title'] = parse_jobpost_receiverTemplateJSON['jobname']
        items['url'] = parse_jobpost_emailletterTemplateJSON['research']
        items['company'] = companyname + " " + finaladdress
        items['location'] = finaladdress
        items['date'] = "date placeholder"
        items['skills'] = skills

        # ### receiverTemplateJSON ################################# #
        receiverTemplateJSON['jobnameinputPrompt'] = "Position:"
        receiverTemplateJSON['jobname'] = parse_jobpost_receiverTemplateJSON['jobname']
        receiverTemplateJSON['jobidinputPrompt'] = "Job Type:"
        receiverTemplateJSON['jobid'] = parse_jobpost_receiverTemplateJSON['jobid']
        receiverTemplateJSON['hours'] = parse_jobpost_receiverTemplateJSON['hours']
        receiverTemplateJSON['name'] = parse_jobpost_receiverTemplateJSON['name']
        receiverTemplateJSON['address'] = finaladdress
        receiverTemplateJSON['city'] = finaladdress
        receiverTemplateJSON['state'] = finaladdress
        receiverTemplateJSON['zip'] = finaladdress
        receiverTemplateJSON['website'] = companyhomepage
        receiverTemplateJSON['attn'] = "meznull"
        receiverTemplateJSON['attnemail'] = parse_jobpost_receiverTemplateJSON['attnemail']
        receiverTemplateJSON['phone'] = "meznull"
        receiverTemplateJSON['situation'] = "Stackoverflow Jobs"

        # ### relationshipTemplateJSON ################################# #
        relationshipTemplateJSON['applicationidentityinputPrompt'] = "applicationidentityinputPrompt"
        relationshipTemplateJSON['applicationidentity'] = parse_jobpost_relationshipTemplateJSON['applicationidentity']
        relationshipTemplateJSON['skillarrayinputPrompt'] = "skillarrayinputPrompt"
        relationshipTemplateJSON['skillarray'] = skills
        relationshipTemplateJSON['knowledgearrayinputPrompt'] = "knowledgearrayinputPrompt"
        relationshipTemplateJSON['knowledgearray'] = skills
        relationshipTemplateJSON['abilityarrayinputPrompt'] = "abilityarrayinputPrompt"
        relationshipTemplateJSON['abilityarray'] = parse_jobpost_relationshipTemplateJSON['abilityarray']

        # ### environmentTemplateJSON ################################# #
        environmentTemplateJSON['companydescriptioninputPrompt'] = "<a href='" + parse_jobpost_emailletterTemplateJSON['research'] + "' target='_blank'>Link: Stackoverflow Job Detail</a>"
        environmentTemplateJSON['companydescription'] = parse_jobpost_environmentTemplateJSON['companydescription']
        environmentTemplateJSON['companyphilosophyinputPrompt'] = "<a href='" + response.request.url + "' target='_blank'>Link: Stackoverflow Company</a>"
        environmentTemplateJSON['companyphilosophy'] = companyphil
        environmentTemplateJSON['companycustomersinputPrompt'] = "Your customers are ..."
        environmentTemplateJSON['companycustomers'] = "Your target industry customers are: " + companytype + ", " + industry
        environmentTemplateJSON['companydistinguishinputPrompt'] = "Something unique to this company..."
        environmentTemplateJSON['companydistinguish'] = "Stackoverflow has tagged your company as: " + companysize

        # ### emailletterTemplateJSON ################################# #
        emailletterTemplateJSON['lead'] = "Scrape Stackoverflow Jobs"
        emailletterTemplateJSON['research'] = parse_jobpost_emailletterTemplateJSON['research']

        self.count = self.count + 1

        yield {
            'id': items['id'],
            'job': items['job'],
            'title': items['title'],
            'url': items['url'],
            'company': items['company'],
            'location': items['location'],
            'date': items['date'],
            'skills': items['skills'],

            "receiverTemplateJSON": receiverTemplateJSON,
            "relationshipTemplateJSON": relationshipTemplateJSON,
            "environmentTemplateJSON": environmentTemplateJSON,
            "emailletterTemplateJSON": {
                "lead": emailletterTemplateJSON['lead'],
                "research": emailletterTemplateJSON['research'],
                "header": "A placeholder for a email header imported from a JSON file.",
                "body": "<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p> <br> Dear <span class=\"highlighterDiv\">{{audience.attn}}</span>, <br><br> <p class='tab'>My name is <span class=\"highlighterDiv\">{{user.firstName}}</span> <span class=\"highlighterDiv\">{{user.lastName}}</span>. I learned about <span class=\"highlighterDiv\">{{audience.name}}</span> though <span class=\"highlighterDiv\">{{leads.leadtype}}</span>. I see you are in the process of hiring for a <span class=\"highlighterDiv\">{{audience.jobname}}</span>. Based on what I learned from <span class=\"highlighterDiv\">{{leads.followup}}</span> you want applicants who have the following skills: <span class=\"highlighterDiv\">{{desirability.skillarray}}}</span>. <span class=\"highlighterDiv\">{{environmentsetting.companydistinguish}}</span>. <span class=\"highlighterDiv\">{{environmentsetting.companycustomers}}</span>. <span class=\"highlighterDiv\">{{environmentsetting.companyphilosophy}}</span>. This position and your company is appealing to me. I would like to talk with you further regarding my eligibility for the <span class=\"highlighterDiv\">{{audience.jobname}}</span>, <span class=\"highlighterDiv\">{{audience.jobid}}</span> position. </p><br><p> Respectfully,</p> <span class = \"highlighterDiv\">{{user.firstName}}</span> <span class = \"highlighterDiv\"> {{user.middleName}} </span> <span class = \"highlighterDiv\">{{user.lastName}}</span> <br> <span class=\"highlighterDiv\">{{user.myUrl}}</span> <p></p>",
                "footer": "A placeholder for a email footer imported from a JSON file."
            },
            "resumeTemplateJSON": {
                "header":"<p align='center'><span class=\"highlighterDiv\">{{user.firstName}} {{user.middleName}} {{user.lastName}}<br>{{user.address}}, {{user.city}}, {{user.state}}, {{user.zip}}<br> {{user.phone}} {{user.email}}</span></p> <h3 align='center'>Resume</h3><hr> <p>I am applying for the <span class=\"highlighterDiv\">{{audience.jobname}}</span> position, <span class=\"highlighterDiv\">{{audience.jobid}}</span>, for <span class=\"highlighterDiv\">{{audience.name}}</span> in <span class=\"highlighterDiv\">{{audience.city}}</span>, <span class=\"highlighterDiv\">{{audience.state}}</span>.</p>",
                "body":"<p><b>Abilities Keyword</b></p><p><center><table><tr><td>Embedded System Analysis</td> <td>Debugging and Troubleshooting</td><td>Testing &amp; Documentation</td></tr><tr><td>Software Development</td><td>Requirements Management</td><td>Project Management</td></tr><tr><td>Coding &amp; Scripting</td><td>GUI Design</td><td>Database Design</td></tr></table></center></p><p><b>Technology Summary</b></p><p> <u>Programming</u>: C, C ++, C#, XML, CSV, SVG, MySQL, MSSql, HTML, VB.Net, ASP.NET, ADO.NET, LINQ, Java, JavaScript, AngularJS, jQuery, CSS, and PHP</p><p><u>Development Tools</u>: Git, Visual Studio, MS Sql Server Management Studio, MySql Workbench, WAMP Server, NetBeans IDE, Atom, Inkscape, Sketchup 3D(CAD)</p><p><u>Systems</u>: Linux, .NET, W3</p><p><b>Education</b></p><p><u>Gannon University Erie, PA | B.S. Electrical/Computer Engineering, 2006</u><br>Electrical Engineering, Computer Engineering, Embedded SystemsPublished Scientific Journal on Artificial Intelligence</p><p></p><p><u>TCC, Tallahassee, FL | (Continued Education) Environmental Science, 2014</u><br>Environmental Systems, Plant Biology, Environmental Law/Regulations</p><p><u>Gannon University Erie, PA | (Masters Schooling) Information Analytics, 2015</u><br>Database Management, Requirements for Software Systems</p><p><b>Professional Experience</b></p><p><u>Independent Green Technologies (IGT) - Tallahassee, FL</u><br>CAD Specialist, 2014</p><p>My responsibility in the company focused on using computer aided design (CAD) tools to model price and cost projections for large-scale commercial organizations and residential stakeholders. The models were used to appraise and simulate design efficiency and feasibility to construct.</p><p><u>United States Coast Guard Cutter Mustang (WPB 1310) - Seward, AK</u><br>Machinery Technician, 2011-2013</p><p>As a member of a ship's engineering staff, I took the initiative to enhance our machinery related catalog and inventory database. Because of this initiative, enhancements were implemented service wide on that ship class. I used MS Access to develop a parts inventory catalog for EATON/Aeroquip brand high pressure hoses. This application was used to manage the preventative maintenance schedule, parts and pricing, and for ordering replacements for worn or damaged equipment and accessory parts.</p><p><u>Coast Guard Station Venice - Venice, LA</u><br>Search and Rescue, Boarding Officer, 2008-2011</p><p>In conjunction with search and rescue response duties, I developed a computer application to enhance safety and productivity. I used my computer technology skills to develop an HTML, CSS and RSS feed based application to gather weather, sea state and tidal information to assist in risk assessment for boats deploying in search and rescue operations.</p>",
                "footer":""
            },
            "coverletterTemplateJSON": {
                "header": "<p class='w3-left-align'>{{today | date}}</p><p><span class=\"highlighterDiv\">{{audience.attn}}</span><br><span class=\"highlighterDiv\">{{audience.name}}</span><br><span class=\"highlighterDiv\">{{audience.address}}</span><br><span class=\"highlighterDiv\">{{audience.city}}</span>, <span class=\"highlighterDiv\">{{audience.state}}</span>, <span class=\"highlighterDiv\">{{audience.zip}}</span></p><br>",
                "body": "<p>Dear <span class=\"highlighterDiv\">{{audience.attn}}</span>,</p> <p class='tab'>My name is <span class=\"highlighterDiv\">{{user.firstName}}</span> <span class=\"highlighterDiv\">{{user.middleName}}</span> <span class=\"highlighterDiv\">{{user.lastName}}</span>. I am applying for the <span class=\"highlighterDiv\">{{audience.jobname}}</span> position, <span class=\"highlighterDiv\">{{audience.jobid}}</span>, for <span class=\"highlighterDiv\">{{audience.name}}</span> in <span class=\"highlighterDiv\">{{audience.city}}</span>, <span class=\"highlighterDiv\">{{audience.state}}</span>. I am seeking to diversify my experience portfolio and build professional relationships as a <span class=\"highlighterDiv\">{{desirability.applicationidentity}}</span>. </p><p class='tab'><span class=\"highlighterDiv\">{{audience.attn}}</span>, thank you for taking the time to consider my application. I hope to be of service to <span class=\"highlighterDiv\">{{audience.name}}</span>.</p>",
                "footer": "<br><p>Sincerely,</p><br><br> <p><span class=\"highlighterDiv\">{{user.firstName}}</span> <span class=\"highlighterDiv\">{{user.middleName}}</span> <span class=\"highlighterDiv\">{{user.lastName}}</span><br><span class=\"highlighterDiv\">{{user.address}}</span>, <span class=\"highlighterDiv\">{{user.city}}</span>, <span class=\"highlighterDiv\">{{user.state}}</span>, <span class=\"highlighterDiv\">{{user.zip}}</span><br><span class=\"highlighterDiv\">{{user.email}}</span></p>"
            }
        }
