from datetime import datetime

import scrapy
import requests

from cloud_project.items.items import JobsVagasItem
from scrapy.http import HtmlResponse

from ..constants.constants import SpidersNames


class ProgramathorSpider(scrapy.Spider):
    name = SpidersNames.PROGRAMATHOR
    start_urls = []
    data = {}
    filter = []
    item = JobsVagasItem()
    # job = ["python", "java", "c", "javascript", "oracle", "rpa", "flutter", "designer"]

    job = ["flutter"]

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
        try:
            job = response.xpath('//h3/text()').getall()
            link = response.xpath('//div[@class="cell-list "]//a/@href').getall()
            employer = response.xpath('//div[@class="cell-list-content-icon"]//span[1]/text()').getall()
            local = response.xpath('//div[@class="cell-list-content-icon"]//span[2]/text()').getall()
            date = datetime.now().strftime("%d/%m/%Y")

            for i in range(len(job)):

                self.item['site'] = SpidersNames.PROGRAMATHOR.capitalize()

                try:
                    self.item['job'] = job[i]
                except:
                    self.item['job'] = ''

                try:
                    self.item['link'] = 'https://programathor.com.br' + link[i]
                except:
                    self.item['link'] = ''

                try:
                    self.item['employer'] = employer[i]
                except:
                    self.item['employer'] = ''

                try:
                    self.item['local'] = local[i]
                except:
                    self.item['local'] = ''

                self.item['date'] = date

                self.item['url'] = response.url

                filter_list = []
                for filter in self.job:
                    if "-" + filter + "?" in self.item['url']:
                        filter_list.append(filter)
                        self.item['filter'] = filter_list

                url = 'https://programathor.com.br' + link[i]

                res = HtmlResponse(url=url, body=requests.get(url).text, encoding='utf-8')

                self.parse_description(res)

                yield self.item


        except IndexError:
            pass

    def parse_description(self, response):
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

        self.item['description'] = description

        # return self.item
