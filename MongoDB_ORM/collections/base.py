import bson
import pymongo
import time
import datetime


class CollectionBase(object):
    def __init__(self, db, collection_name):
        self.collection = db[collection_name]
        self.ASCENDING = pymongo.ASCENDING
        self.DESCENDING = pymongo.DESCENDING

    def ObjectId(self, doc_id):
        return bson.objectid.ObjectId(doc_id)

    def timestamp(self):
        now = datetime.datetime.now()
        return time.mktime(now.timetuple())

    async def find_one_by_id(self, doc_id):
        condition = {'_id': self.ObjectId(doc_id)}
        return await self.collection.find_one(condition)

    def find_all(self):
        return self.collection.find({})

    def find_pages_by_id(self, condition, sort, page, pagesize):
        limit = pagesize
        skip = (page - 1) * pagesize
        cursor = self.collection.find(condition, limit=limit, skip=skip, sort=sort)
        return cursor

    async def insert_one(self, doc):
        await self.collection.insert(doc)

    async def update_one_by_id(self, doc_id, doc):
        condition = {'_id': self.ObjectId(doc_id)}
        doc = {'$set': doc}
        await self.collection.update_one(condition, doc)

    async def delete_one_by_id(self, doc_id):
        condition = {'_id': self.ObjectId(doc_id)}
        await self.collection.delete(condition)
