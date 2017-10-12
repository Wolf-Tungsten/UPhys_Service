from .base import ObjectId,MongodbOrmBase


class Category(MongodbOrmBase):
    def __init__(self, mongo_control):
        MongodbOrmBase.__init__(self, mongo_control)
        self.colName = 'category'

    async def update(self, id, behave):
        condition = {'_id': ObjectId(id)}
        behave = {'$set': behave}
        await self.db.update(condition, behave, self.colName)

    async def get_behave_free(self, condition, sortby, sort, limit, skip):
        behavelist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        return behavelist

    async def get_by_id(self, id):
        condition = {'_id': ObjectId(id)}
        behave = await self.db.get_document_one(condition, self.colName)
        return behave

    async def insert(self, behave):
        result = await self.db.insert(behave, self.colName)
        return result

    async def delete(self, behave_id):
        condition = {'_id': behave_id}
        await self.db.delete(condition, self.colName)

    def brief_behave(self, behave):
        briefbehave = self.db.brief_behave(behave)
        return briefbehave
