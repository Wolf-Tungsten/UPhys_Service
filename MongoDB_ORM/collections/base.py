import bson


class CollectionBase(object):
    def __init__(self, db, collection_name):
        self.collection = db[collection_name]

    def ObjectId(self, doc_id):
        return bson.objectid.ObjectId(doc_id)

    async def find_one_by_id(self, doc_id):
        condition = {'_id': self.ObjectId(doc_id)}
        return await self.collection.find_one(condition)

    def find_all(self):
        return self.collection.find({})

    async def insert_one(self, doc):
        await self.collection.insert(doc)

    async def update_one_by_id(self, doc_id, doc):
        condition = {'_id': self.ObjectId(doc_id)}
        doc = {'$set': doc}
        await self.collection.update_one(condition, doc)

    async def delete_one_by_id(self, doc_id):
        condition = {'_id': self.ObjectId(doc_id)}
        await self.collection.delete(condition)
