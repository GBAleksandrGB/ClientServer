import pymongo


class JobparserPipeline:
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE', 'hhjp'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item not in self.db[self.collection_name].find({}):
            self.db[self.collection_name].update_one({'name': item['name'],
                                                      'salary': item['salary'],
                                                      'employer': item['employer'],
                                                      'ref': item['ref']},
                                                     {'$set': dict(item)},
                                                     True)
        return item
