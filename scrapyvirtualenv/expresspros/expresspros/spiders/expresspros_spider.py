import scrapy
from expresspros.items import ExpressprosItem

import datetime

class ExpressprosSpider(scrapy.Spider):
    name = "expresspros"
    allowed_domain = ["https://www.expresspros.com/"]
    # start_urls = ["https://workforce.expresspros.com/locations/state/Alabama", "https://workforce.expresspros.com/locations/state/Georgia", "https://workforce.expresspros.com/locations/state/Florida"]

    count = 0

    def __init__(self, domain='', *args,**kwargs):
        super(ExpressprosSpider, self).__init__(*args, **kwargs)
        domain = domain.split(',')
        self.start_urls = domain

    # tutorial guidance: https://doc.scrapy.org/en/latest/intro/tutorial.html#more-examples-and-patterns
    def parse(self, response):
        # scrape contact info
        for sel in response.xpath('//div[@class="row location-item"][@style="padding-bottom: 15px;"]'):
            item = ExpressprosItem()

            tempAddrArr = [i.strip() for i in sel.xpath('div/div/div/text()').extract()]
            tempAddrArr = ", ".join(tempAddrArr)

            item['officeCity'] = sel.xpath('h4/text()').extract_first()
            item['officeAddress'] = tempAddrArr
            item['officePhone'] = sel.xpath('div[1]/div[2]/a/@href').extract_first()
            item['officeEmail'] = sel.xpath('div[2]/div[1]/a/@href').extract_first()
            item['officeWeb'] = sel.xpath('div[2]/div[3]/a/@href').extract_first()

        # follow links to city pages
        for href in response.xpath('//div[@class="row location-item"][@style="padding-bottom: 15px;"]/div[2]/div[3]/a/@href'):
            if (href):
                yield response.follow(href, self.parse_city, meta={'item':item})

    # scrape the page the link led me to
    def parse_city(self, response):
        item = response.meta['item']

        for sel in response.css('div.widgetBody > div.row'):
            title = sel.css('div.col-sm-7 h3::text').extract_first()
            company = sel.css('div.col-sm-3 h3::text').extract_first().strip()
            company = company.replace(',A', ', A')
            company = company.replace(',F', ', F')
            company = company.replace(',G', ', G')

            addressArray = item['officeAddress'].split(',')
            addressArrayLength = len(addressArray)

            if (addressArrayLength == 3):
                addressStreet = addressArray[0]
                addressApt = ""
                addressCity = addressArray[1]

                addressState = addressArray[2]
                addressState = addressState.replace(' ', '')

                addressZip = addressState.split(' ')
                addressZip = addressZip[2]
            elif (addressArrayLength == 4):
                addressStreet = addressArray[0]
                addressApt = addressArray[1]
                addressCity = addressArray[2]
                addressState = addressArray[3]
                addressState = addressState.split(' ')
                addressZip = addressState[2]
                addressState = addressState[1]
            else:
                addressStreet = str(addressArrayLength)
                addressApt = str(addressArrayLength)
                addressCity = "addressArray[1]" + str(addressArrayLength)

                addressState = "addressArray[2]" + str(addressArrayLength)
                addressState = "addressState.replace(' ', '')" + str(addressArrayLength)

                addressZip = "addressState.split(' ')" + str(addressArrayLength)
                addressZip = "addressZip[2]" + str(addressArrayLength)

            self.count = self.count + 1

            yield {
                'id': self.count,
                'spider': "expresspros",
                'title': title,
                'url': sel.css('a.btn::attr(href)').extract_first(),
                'company': company,
                'date': datetime.datetime.now().strftime ("%Y%m%d"),
                'address': item['officeAddress'],
                # document-writer json
                "senderTemplateJSON": {
                    "firstName": "Mezcel",
                    "middleName": "",
                    "lastName": "Matters",
                    "address": "123 Address Ln.",
                    "city": "Sim City",
                    "state": "ST",
                    "zip": "12345",
                    "phone": "123-456-7890",
                    "email": "mezcel@mail.com",
                    "myUrl": "https://github.com/mezcel"
                },
                "receiverTemplateJSON": {
                    "jobnameinputPrompt":"Position:",
                    "jobname": title,
                    "jobidinputPrompt":"Job Type:",
                    "jobid": "na",
                    "hours": "1",
                    "name": "Express Pros: " + company,
                    "address": addressStreet + addressApt,
                    "city": addressCity,
                    "state": addressState,
                    "zip": addressZip,
                    "website": item['officeWeb'],
                    "attn": "Express Pros: " + company,
                    "attnemail": item['officeEmail'],
                    "phone": item['officePhone'],
                    "situation":"Express Pros Online"
                },
                "environmentTemplateJSON": {
                    "companydescriptioninputPrompt": "na",
                    "companydescription": "na",
                    "companyphilosophyinputPrompt": "na",
                    "companyphilosophy": "na",
                    "companycustomersinputPrompt": "na",
                    "companycustomers": "na",
                    "companydistinguishinputPrompt": "na",
                    "companydistinguish": "na"
                },
                "relationshipTemplateJSON": {
                    "applicationidentityinputPrompt": "na",
                    "applicationidentity": "na",
                    "skillarrayinputPrompt": "na",
                    "skillarray": "na",
                    "knowledgearrayinputPrompt":"... , and I ...",
                    "knowledgearray": "na",
                    "abilityarrayinputPrompt":"... , my abilities include ...",
                    "abilityarray": "na"
                },
            	"emailletterTemplateJSON": {
            		"lead":"Express Pros Website",
            		"research":"life experience and observations",
            		"header":"Express Pros Office",
            		"body":"<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p> <br> Dear <span class='highlighterDiv'>{{audience.attn}}</span>, <br><br> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I learned about your company, <span class='highlighterDiv'>{{audience.name}}</span>, through <span class='highlighterDiv'>{{leads.leadtype}}</span>. I understand you are currently in the process of hiring a <span class='highlighterDiv'>{{audience.jobname}}</span>. I am seeking employment in this discipline of technology. Based on what I learned from <span class='highlighterDiv'>{{leads.followup}}</span>, I see that your company <span class='highlighterDiv'>{{environmentsetting.companydescription}}</span>. Your customers <span class='highlighterDiv'>{{environmentsetting.companycustomers}}</span>. You are looking for talent who have skills in <span class = 'highlighterDiv' >{{desirability.skillarray}}</span>. Your organization <span class='highlighterDiv'>{{environmentsetting.companyphilosophy}}</span>. <span class='highlighterDiv'>{{environmentsetting.companydistinguish}}</span>. This appeals to me, and I would like the opportunity to try out for your team.</p>",
            		"footer":"A placeholder for a email footer imported from a JSON file."
            	},
            	"resumeTemplateJSON": {
            		"header":"<p align='center'><span class='highlighterDiv'>{{user.firstName}} {{user.middleName}} {{user.lastName}}<br>{{user.address}}, {{user.city}}, {{user.state}}, {{user.zip}}<br> {{user.phone}} {{user.email}}</span></p> <h3 align='center'>Resume</h3><hr> <p>I am applying for the <span class='highlighterDiv'>{{audience.jobname}}</span> position, <span class='highlighterDiv'>{{audience.jobid}}</span>, for <span class='highlighterDiv'>{{audience.name}}</span> in <span class='highlighterDiv'>{{audience.city}}</span>, <span class='highlighterDiv'>{{audience.state}}</span>.</p>",
            		"body":"<p><b>Services</b></p><p><center><table><tr><td>Embedded System Analysis</td><td>Debugging &amp; Troubleshooting</td><td>Testing &amp; Documentation</td></tr><tr><td>Software Development</td><td>Requirements Management</td><td>Project Management</td></tr><tr><td>Coding &amp; Scripting</td><td>GUI Design</td><td>Database Design</td></tr></table></center></p>",
            		"footer":"A placeholder for a resume footer imported from a JSON file."
            	},
            	"coverletterTemplateJSON": {
            		"header": "<p id='coverletterTime' class='w3-left-align'>{{today | date}}</p><p><span class='highlighterDiv'>{{audience.attn}}</span><br><span class='highlighterDiv'>{{audience.name}}</span><br><span class='highlighterDiv'>{{audience.address}}</span><br><span class='highlighterDiv'>{{audience.city}}</span>, <span class='highlighterDiv'>{{audience.state}}</span>, <span class='highlighterDiv'>{{audience.zip}}</span></p><br>",
            		"body": "<p>Dear <span class='highlighterDiv'>{{audience.attn}}</span>,</p> <p class='tab'>My name is <span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.middleName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span>. I am applying for the <span class='highlighterDiv'>{{audience.jobname}}</span> position at <span class='highlighterDiv'>{{audience.name}}</span>, in <span class='highlighterDiv'>{{audience.city}}</span>. I possess skills in <span class='highlighterDiv'>{{desirability.skillarray}}</span>. As a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>, my abilities include <span class='highlighterDiv'>{{desirability.abilityarray}}</span>, and I <span class='highlighterDiv'>{{desirability.knowledgearray}}</span>.</p> <p class='tab'>I am seeking to diversify my technology portfolio and develop a career as a <span class='highlighterDiv'>{{desirability.applicationidentity}}</span>.</p><p class='tab'><span class='highlighterDiv'>{{audience.attn}}</span>, thank you for taking the time to read and consider my cover letter for employment with <span class='highlighterDiv'>{{audience.name}}</span>. I have multiple technical skills an diverse work experiences that will integrate well within your organization and its business culture. I welcome the opportunity to discuss your observations and my prospects of joining your organization and making an immediate contribution to your productivity.</p> ",
            		"footer": "<p>Sincerely,</p><br><br> <p><span class='highlighterDiv'>{{user.firstName}}</span> <span class='highlighterDiv'>{{user.middleName}}</span> <span class='highlighterDiv'>{{user.lastName}}</span><br><span class='highlighterDiv'>{{user.address}}</span>, <span class='highlighterDiv'>{{user.city}}</span>, <span class='highlighterDiv'>{{user.state}}</span>, <span class='highlighterDiv'>{{user.zip}}</span><br><span class='highlighterDiv'>{{user.email}}</span></p>"
            	}
            }
