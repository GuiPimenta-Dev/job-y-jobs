# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapyd_client.commands import schedule


class LoginVagasItem(scrapy.Item):
    status = scrapy.Field()


class JobsVagasItem(scrapy.Item):
    site = scrapy.Field()
    job = scrapy.Field()
    link = scrapy.Field()
    employer = scrapy.Field()
    description = scrapy.Field()
    local = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    filter = scrapy.Field()
    timestamp = scrapy.Field()
