# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import pymongo


class CloudProjectPipeline:

    def __init__(self):

        #VARIAVEIS AMBIENTE DO HEROKU
        self.conn = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['USER']}:{os.environ['PASS']}@backend.lwkqa.mongodb.net/{os.environ['DB']}?retryWrites={os.environ['RETRY']}&w=majority")


        # TODO trocar novamente para jobs_Tb depois

        db = self.conn.jobs

        self.collection = db[os.environ['COLLECTION']]

    def process_item(self, item, spider):
        if not self.collection.find_one({"link": item['link']}):
            self.collection.insert(dict(item))
        return item
