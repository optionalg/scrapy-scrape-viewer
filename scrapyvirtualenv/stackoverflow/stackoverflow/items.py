# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StackoverflowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    id= scrapy.Field()
    job= scrapy.Field()
    title= scrapy.Field()
    url= scrapy.Field()
    company= scrapy.Field()
    location= scrapy.Field()
    date= scrapy.Field()
    skills= scrapy.Field()

    loopCounter = scrapy.Field()
    firstName = scrapy.Field()
    middleName = scrapy.Field()
    lastName = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    myUrl = scrapy.Field()
    jobnameinputPrompt = scrapy.Field()
    jobname = scrapy.Field()
    jobidinputPrompt = scrapy.Field()
    jobid = scrapy.Field()
    hours = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    website = scrapy.Field()
    attn = scrapy.Field()
    attnemail = scrapy.Field()
    phone = scrapy.Field()
    situation = scrapy.Field()
    companydescriptioninputPrompt = scrapy.Field()
    companydescription = scrapy.Field()
    companyphilosophyinputPrompt = scrapy.Field()
    companyphilosophy = scrapy.Field()
    companycustomersinputPrompt = scrapy.Field()
    companycustomers = scrapy.Field()
    companydistinguishinputPrompt = scrapy.Field()
    companydistinguish = scrapy.Field()
    applicationidentityinputPrompt = scrapy.Field()
    applicationidentity = scrapy.Field()
    skillarrayinputPrompt = scrapy.Field()
    skillarray = scrapy.Field()
    knowledgearrayinputPrompt = scrapy.Field()
    knowledgearray = scrapy.Field()
    abilityarrayinputPrompt = scrapy.Field()
    abilityarray = scrapy.Field()
    lead = scrapy.Field()
    research = scrapy.Field()
    header = scrapy.Field()
    body = scrapy.Field()
    footer = scrapy.Field()

    pass
