from datetime import datetime

import scrapy
from scrapy.http.request import Request
from scrapy.http import Response
from inline_requests import inline_requests

from cloud_project.items.items import JobsVagasItem

from ..constants.constants import SpidersNames


class ProgramathorSpider(scrapy.Spider):
    name = SpidersNames.PROGRAMATHOR
    start_urls = []
    data = {}
    job = ["python", "java", "c#", "javascript", "oracle", "rpa", "flutter", "designer"]

    # job = ["Python"]

    def __init__(self, *args, **kwargs):

        for job in self.job:
            start_urls = [f'https://programathor.com.br/jobs-{job.lower()}?page={i}' for i in range(1, 10)]
            # start_urls = ['https://programathor.com.br/jobs/15491-desenvolvedor-a-mobile-flutter']
            for start_url in start_urls:
                self.start_urls.append(start_url)
                self.data[job] = 0
        self.logger.info(self.start_urls)
        super(ProgramathorSpider, self).__init__(*args, **kwargs)


    def parse(self, response, **kwargs):
        item = JobsVagasItem()
        divs = response.xpath('//div[@class="cell-list "]')

        job = response.xpath('//h3/text()').getall()
        link = response.xpath('//div[@class="cell-list "]//a/@href').getall()
        employer = response.xpath('//div[@class="cell-list-content-icon"]//span[1]/text()').getall()
        local = response.xpath('//div[@class="cell-list-content-icon"]//span[2]/text()').getall()
        date = datetime.now().strftime("%d/%m/%Y")

        for i in range(len(link)):
            # job = i.xpath('//h3/text()').get()
            # link = 'https://programathor.com.br' + i.xpath('//div[@class="cell-list "]//a/@href').get()
            # employer = i.xpath('//div[@class="cell-list-content-icon"]//span[1]/text()').get()
            # local = i.xpath('//div[@class="cell-list-content-icon"]//span[2]/text()').get()
            # date = datetime.now().strftime("%d/%m/%Y")

            item['site'] = SpidersNames.PROGRAMATHOR.capitalize()

            try:
                item['job'] = job[i]
            except:
                item['job'] = ''

            try:
                item['link'] =  'https://programathor.com.br'+ link[i]
            except:
                item['link'] = ''

            try:
                item['employer'] = employer[i]
            except:
                item['employer'] = ''

            try:
                item['local'] = local[i]
            except:
                item['local'] = ''

            item['date'] = date

            item['url'] = response.url

            for job in self.job:
                if "-" + job + "?" in item['url']:
                    item['filter'] = job

            # yield item
            url = 'https://programathor.com.br'+ link[i]
            yield scrapy.Request(url='https://programathor.com.br'+ link[i], callback=self.parse_description,meta={"item": item})

    #
    def parse_description(self, response: Response):
        company_description1 = response.xpath('//p[4]/text()').getall()
        company_description2 = response.xpath('//p[5]/text()').getall()
        activities = response.xpath('//p[6]/text()').getall()
        requisites = response.xpath('//p[9]/text()').getall()
        wished = response.xpath('//p[10]/text()').getall()
        college = response.xpath('//p[11]/text()').getall()

        description = ''

        if company_description1:
            for i in company_description1:
                description += i

        if company_description2:
            for i in company_description1:
                description += i

        if activities:
            for i in activities:
                description += i

        if requisites:
            for i in requisites:
                description += i

        if wished:
            for i in wished:
                description += i

        if college:
            for i in college:
                description += i

        item = response.meta['item']
        item['description'] = description

        return item
