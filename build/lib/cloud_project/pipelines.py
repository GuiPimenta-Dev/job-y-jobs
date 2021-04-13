# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo


class CloudProjectPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient(
            "mongodb+srv://GuilhermePimenta:guilherme27@backend.lwkqa.mongodb.net/BackEnd?retryWrites=true&w=majority")
        db = self.conn.jobs

        # self.conn = pymongo.MongoClient(
        #     'localhost',
        #     27017
        # )
        # db = self.conn['jobs']

        self.collection = db['jobs_tb']

    def process_item(self, item, spider):
        if not self.collection.find_one({"link": item['link']}):
            self.collection.insert(dict(item))
        return item
