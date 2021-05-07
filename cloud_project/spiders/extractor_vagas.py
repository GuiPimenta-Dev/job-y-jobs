import scrapy

from cloud_project.items.items import JobsVagasItem
from ..constants.constants import SpidersNames


class VagasSpider(scrapy.Spider):
    name = SpidersNames.VAGAS
    start_urls = []
    data = {}
    item = JobsVagasItem()
    # job = ["python", "java", "c", "javascript", "oracle", "rpa", "flutter", "designer"]

    job = ["flutter","rpa"]

    def __init__(self, *args, **kwargs):

        # jobs_param = kwargs.pop('job', [])
        # job_list = jobs_param.split(',')

        for job in self.job:
            start_urls = [f'https://www.vagas.com.br/vagas-de-{job}?pagina={i}' for i in range(1, 10)]
            for start_url in start_urls:
                self.start_urls.append(start_url)
                self.data[job] = 0

        self.logger.info(self.start_urls)
        super(VagasSpider, self).__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        for i in response.xpath('//li[contains(@class, "vaga odd ") or contains(@class, "vaga even ")]'):

            self.item['site'] = "Vagas.com"

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
                description_list = i.xpath(
                    './/div[@class="detalhes"]//p/text() | .//div[@class="detalhes"]//p//mark/text()').extract()
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

            filter_list = []
            for filter in self.job:
                if "-" + filter + "?" in self.item['url']:
                    filter_list.append(filter)
                    self.item['filter'] = filter_list

            self.item['url'] = response.url

            yield self.item





