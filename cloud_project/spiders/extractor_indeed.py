import scrapy

from cloud_project.items.items import JobsVagasItem


class ExtractorIndeedSpider(scrapy.Spider):
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
            for start_url in start_urls:
                self.start_urls.append(start_url)
        self.logger.info(self.start_urls)
        super(ExtractorIndeedSpider, self).__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        ids = response.xpath(
            '//table[@id="resultsBody"]//div[@class="jobsearch-SerpJobCard unifiedRow row result"]/@id').extract()
        for i in ids:
            job = response.xpath(f'//div[@id="{i}"]//h2//a/@title').get()
            link = response.xpath(f'//div[@id="{i}"]//h2//a/@id').get()
            link_href = response.xpath(f'//div[@id="{i}"]//h2//a/@href').get()
            employer = response.xpath(f'//div[@id="{i}"]//span[@class="company"]/text()').get()
            employer_a = response.xpath(f'//div[@id="{i}"]//span[@class="company"]//a/text()').get()
            description = response.xpath(f'//div[@id="{i}"]//div[@class="summary"]/text()').get()
            description_ul= response.xpath(
                f'//div[@id="{i}"]//div[@class="summary"]//li/text() | //div[@id="{i}"]//div[@class="summary"]//li//b/text() ').extract()
            local = response.xpath(f'//div[@id="{i}"]//div[@class="recJobLoc"]/@data-rc-loc').get()
            date = response.xpath(f'//div[@id="{i}"]//div[@class="result-link-bar"]/span/text()').get()

            if employer is not None:
                employer = employer.strip()

            if employer_a is not None:
                employer_a = employer_a.strip()

            if description is not None:
                description = description.strip()

            self.item['site'] = "Indeed"

            try:
                self.item['job'] = job
            except:
                self.item['job'] = ''
            try:
                if "sja" not in link:
                    self.item['link'] = response.url + "&vjk=" + link.split('_')[1]
                else:
                    self.item['link'] = 'https://br.indeed.com' + link_href
            except:
                self.item['link'] = ''
            try:
                if employer is not None or employer_a is not None:
                    if employer:
                        self.item['employer'] = employer
                    else:
                        self.item['employer'] = employer_a
                else:
                    self.item['employer'] = 'Não informado'
            except:
                self.item['employer'] = ''

            try:
                if description is not None or description_ul is not None:
                    if description:
                        self.item['description'] = description
                    else:
                        self.item['description'] = '\n'.join(description_ul)

                else:
                    self.item['description'] = 'Não informado'
            except:
                self.item['description'] = ''

            try:
                self.item['local'] = local
            except:
                self.item['local'] = ''

            try:
                self.item['date'] = date
            except:
                self.item['date'] = ''

            yield self.item

