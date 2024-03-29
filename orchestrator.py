# -*- coding: utf-8 -*-
from DateTime.pytz_support import hour
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from cloud_project.spiders.extractor_vagas import VagasSpider
from cloud_project.spiders.extractor_indeed import IndeedSpider
from cloud_project.spiders.extractor_programathor import ProgramathorSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[VagasSpider], hours=4)
scheduler.add_job(process.crawl, 'interval', args=[IndeedSpider], days=7)
scheduler.add_job(process.crawl, 'interval', args=[IndeedSpider], hours=4)

scheduler.start()
process.start(False)

















# import threading
# from scrapy.crawler import CrawlerRunner
# import schedule
# import time
# from spiders.extractor_vagas import ExtractorVagasSpider
#
#
# def run_crawl():
#     runner = CrawlerRunner()
#     runner.crawl(ExtractorVagasSpider)
#
# schedule.every(10).seconds.do(run_crawl)
# # schedule.every().day.at("10:28").do(run_crawl)
#
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)


# def job():
#     print(f'Estou rodando na thread {threading.current_thread()}')
#
# def run_threaded(job_func):
#     job_thread = threading.Thread(target=job_func)
#     job_thread.start()


# schedule.every(10).seconds.do(run_threaded,job)
# schedule.every(10).seconds.do(run_threaded,job)
# schedule.every(10).seconds.do(run_threaded,job)
# schedule.every(10).seconds.do(run_threaded,job)
# schedule.every().day.at("10:24").do(run_threaded,job)
