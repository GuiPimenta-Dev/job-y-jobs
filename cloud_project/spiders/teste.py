# import scrapy
# from scrapy.crawler import CrawlerProcess
#
#
# class Scraper(scrapy.Spider):
#     name = "Scraper"
#     start_urls = [
#         'https://en.wikipedia.org/wiki/Web_scraping',
#     ]
#
#     def parse(self, response):
#         for next_page in response.css('div.mw-parser-output > p > a'):
#             yield response.follow(next_page, self.parse)
#
#         for quote in response.css('div.mw-parser-output > p'):
#             yield {'quote': quote.extract()}
#
#
# process = CrawlerProcess()
# process.crawl(Scraper)
# process.start()