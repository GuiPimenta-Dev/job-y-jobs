# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from cloud_project.spiders.extractor_vagas import ExtractorVagasSpider


process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
# scheduler.add_job(process.crawl, 'cron', args=[ExtractorVagasSpider], day="*",hour="16",minute="18")
scheduler.add_job(process.crawl, 'cron', args=[ExtractorVagasSpider], day="*",hour="22",minute="50")
# scheduler.add_job(process.crawl, 'interval', args=[ExtractorVagasSpider], minutes=5)


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






