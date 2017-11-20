import bson
import pymongo
import time
import datetime
import asyncio


class CollectionBase(object):
    def __init__(self, db, collection_name):
        self.collection = db[collection_name]
        self.ASCENDING = pymongo.ASCENDING
        self.DESCENDING = pymongo.DESCENDING
        self.db = db  # 为了让集合之间可以交错，虽然我表示很不舒服
        self.default = {}

    def get_default(self):
        default = {}
        for k in self.default:
            default[k] = self.default[k]
        return default

    def ObjectId(self, doc_id):
        return bson.objectid.ObjectId(doc_id)

    def timestamp(self):
        now = datetime.datetime.now()
        return time.mktime(now.timetuple())

    async def find_one_by_id(self, doc_id):
        condition = {'_id': self.ObjectId(doc_id)}
        doc = await self.collection.find_one(condition)
        if doc is not None:
            doc['_id'] = str(doc['_id'])
        return doc

    async def find_all(self):
        cursor = self.collection.find({})
        result = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result

    async def find_by_condition(self, condition):
        cursor = self.collection.find(condition)
        result = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result

    async def find_pages_by_condition(self, condition, sort, page, pagesize):
        page = int(page)
        pagesize = int(pagesize)
        limit = pagesize
        skip = (page - 1) * pagesize
        cursor = self.collection.find(condition, limit=limit, skip=skip, sort=sort)
        result = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result

    async def insert_one(self, doc):
        await self.collection.insert(doc)

    async def update_one_by_id(self, doc_id, doc):
        condition = {'_id': self.ObjectId(doc_id)}
        if '_id' in doc:
            doc.pop('_id') #  !!存在隐患
        doc = {'$set': doc}
        await self.collection.update_one(condition, doc)

    async def delete_one_by_id(self, doc_id):
        condition = {'_id': self.ObjectId(doc_id)}
        await self.collection.delete_one(condition)

    async def delete_by_condition(self, condition):
        await self.collection.delete_many(condition)

    async def get_count_by_condition(self, condition):
        return await self.collection.count(condition)

    async def user_info(self, user_id):
        user_id = self.ObjectId(user_id)
        condition = {'_id': user_id}
        return await self.db['user'].find_one(condition)
