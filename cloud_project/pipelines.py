# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from cloud_project.constants.constants import SpidersNames

import pymongo
# from env import USER, PASS, DB, RETRY, COLLECTION


class CloudProjectPipeline:

    def __init__(self):
        # VARIAVEIS AMBIENTE DO HEROKU
        self.conn = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['USER']}:{os.environ['PASS']}@backend.lwkqa.mongodb.net/{os.environ['DB']}?retryWrites={os.environ['RETRY']}&w=majority")

        # VARIAVEIS .ENV
        # self.conn = pymongo.MongoClient(
        #     f"mongodb+srv://{USER}:{PASS}@backend.lwkqa.mongodb.net/{DB}?retryWrites={RETRY}&w=majority")

        db = self.conn.jobs

        self.collection_jobs_tb = db[os.environ['COLLECTION']]
        # self.collection_jobs_tb = db[COLLECTION]
        # self.collection_summary = db["summary"]

    def process_item(self, item, spider):

        if not self.collection_jobs_tb.find_one({"link": item['link']}):
            self.collection_jobs_tb.insert(dict(item))

            if spider.name == SpidersNames.VAGAS:
                for job in spider.job:
                    if "-" + job + "?" in item['url']:
                        spider.data[job] += 1

            if spider.name == SpidersNames.PROGRAMATHOR:
                for job in spider.job:
                    if "-" + job + "?" in item['url']:
                        spider.data[job] += 1

        return item
