import scrapy

from cloud_project.items.vagas.items import JobsVagasItem

import datetime
from scrapy.http import HtmlResponse


class ExtractorVagasSpider(scrapy.Spider):
    name = 'spider_jobs_indeed'
    start_urls = []
    item = JobsVagasItem()
    job = ["Python", "Java", "C#", "JavaScript", "Oracle", "RPA", "Flutter", "Designer"]

    # job = ["Python"]

    def __init__(self, *args, **kwargs):

        # jobs_param = kwargs.pop('job', [])
        # job_list = jobs_param.split(',')

        for job in self.job:
            start_urls = [f'https://br.indeed.com/empregos?q={job}&start={i}' for i in range(0, 100, 10)]
            # start_urls = [f'https://br.indeed.com/jobs?q=Python&start=20']
            for start_url in start_urls:
                self.start_urls.append(start_url)
        self.logger.info(self.start_urls)
        super(ExtractorVagasSpider, self).__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        job = response.xpath('//h2//a/@title').extract()
        link = response.xpath('//h2//a/@id').extract()
        employer = list(filter(None, list(map(str.strip, response.xpath(
            '//span[@class="company"]/text() | //span[@class="company"]//a/text()').extract()))))

        description = list(filter(None, list(map(str.strip, response.xpath(
            '//div[@class="summary"]//ul | //div[@class="summary"]/text()').extract()))))

        local = response.xpath('//div[@class="recJobLoc"]/@data-rc-loc').extract()
        date = response.xpath('//div[@class="result-link-bar"]/span/text()').extract()

        for i in range(len(job)):
            try:
                self.item['job'] = job[i]
            except:
                self.item['job'] = ''
            try:
                self.item['link'] = response.url + "&vjk=" + link[3].split('_')[1]
            except:
                self.item['link'] = ''
            try:
                self.item['employer'] = employer[i]
            except:
                self.item['employer'] = ''

            try:
                self.item['description'] = description[i]
            except:
                self.item['description'] = ''

            try:
                self.item['local'] = local[i]
            except:
                self.item['local'] = ''
            try:
                self.item['date'] = date[i]
            except:
                self.item['date'] = ''

            yield self.item
