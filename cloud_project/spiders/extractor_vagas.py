import scrapy
from scrapy.crawler import CrawlerProcess

from cloud_project.items.vagas.items import JobsVagasItem

class ExtractorVagasSpider(scrapy.Spider):
    name = 'spider_jobs_vagas'
    start_urls = []
    item = JobsVagasItem()
    # job = ["Python", "Java", "C#", "JavaScript", "Oracle", "RPA", "Flutter", "Designer"]
    job = ["Python"]

    def __init__(self, *args, **kwargs):

        # jobs_param = kwargs.pop('job', [])
        # job_list = jobs_param.split(',')

        for job in self.job:
            start_urls = [f'https://www.vagas.com.br/vagas-de-{job}?pagina={i}' for i in range(1, 10)]
            for start_url in start_urls:
                self.start_urls.append(start_url)
        self.logger.info(self.start_urls)
        super(ExtractorVagasSpider, self).__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        for i in response.xpath('//li[contains(@class, "vaga odd ") or contains(@class, "vaga even ")]'):

            try:
                self.item['job'] = i.xpath('.//h2[@class="cargo"]/a/@title').get()
            except:
                self.item['job'] = ''
            try:
                self.item['link'] = 'https://www.vagas.com.br' + i.xpath('.//h2[@class="cargo"]/a/@href').get()
            except:
                self.item['link'] = ''
            try:
                self.item['employer'] = i.xpath('.//span[@class="emprVaga"]/text()').get().strip()
            except:
                self.item['employer'] = ''
            try:
                description_list = i.xpath('.//div[@class="detalhes"]//p/text() | .//div[@class="detalhes"]//p//mark/text()').extract()
                self.item['description'] = ' '.join(description_list)
            except:
                self.item['description'] = ''
            try:
                self.item['local'] = i.xpath('.//footer/span/text()').extract()[1].strip()
            except:
                self.item['local'] = ''
            try:
                self.item['date'] = i.xpath('.//footer/span/text()').extract()[2]
            except:
                self.item['date'] = ''

            yield self.item

