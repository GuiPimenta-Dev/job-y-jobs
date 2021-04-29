# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import pymongo

# from env import USER,PASS,DB,RETRY,COLLECTION
USER = "GuilhermePimenta"
PASS = "guilherme27"
DB = "BackEnd"
RETRY = "true"
COLLECTION = "jobs_tb"

class CloudProjectPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['USER']}:{os.environ['PASS']}@backend.lwkqa.mongodb.net/{os.environ['DB']}?retryWrites={os.environ['Retry']}&w=majority")
        # self.conn = pymongo.MongoClient(
        #     f"mongodb+srv://{USER}:{PASS}@backend.lwkqa.mongodb.net/{DB}?retryWrites={RETRY}&w=majority")

        # TODO trocar novamente para jobs_Tb depois

        db = self.conn.jobs

        self.collection = db[COLLECTION]

    def process_item(self, item, spider):
        if not self.collection.find_one({"link": item['link']}):
            self.collection.insert(dict(item))
        return item
