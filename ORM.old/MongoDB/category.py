from .base import ObjectId, MongodbOrmBase


class Category(MongodbOrmBase):
    def __init__(self, mongodb_control):
        MongodbOrmBase.__init__(self, mongodb_control)

    # GET /categories
    async def get_categories(self):
        return self.db.find()

    # GET /category
    async def get_category(self, category_id):
        return await self.get_by_id(category_id)

    # POST /category
    async def post_category(self, category):
        return await self.insert(category)

    # PUT /category
    async def put_category(self, category_id, category):
        await self.update(category_id, category)

    # DELETE /category
    async def delete_category(self, category_id):
        await self.delete(category_id)


    async def update(self, category_id, category):
        condition = {'_id': ObjectId(category_id)}
        category = {'$set': category}
        await self.db.update(condition, category, self.colName)

    async def get_behave_free(self, condition, sortby, sort, limit, skip):
        behavelist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        return behavelist

    async def get_by_id(self, id):
        condition = {'_id': ObjectId(id)}
        category = await self.db.get_document_one(condition, self.colName)
        return category

    async def insert(self, behave):
        result = await self.db.insert(behave, self.colName)
        return result

    async def delete(self, behave_id):
        condition = {'_id': behave_id}
        await self.db.delete(condition, self.colName)


