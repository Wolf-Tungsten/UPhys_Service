from MongoDB_ORM.collections.base import CollectionBase


class Category(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'category')

    # GET /categories
    async def get_categories(self, privilege):
        condition = {'privilege': {'$lt': privilege + 1}}
        cursor = self.collection.find(condition)
        result = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result

    # GET /category
    async def get_category(self, category_id,privilege):
        result = await self.find_one_by_id(category_id)
        if result['privilege'] <= privilege:
            return result
        return {}

    # POST /category
    async def post_category(self, category):
        return await self.insert_one(category)

    # PUT /category
    async def put_category(self, category_id, category):
        await self.update_one_by_id(category_id, category)

    # DELETE /category
    async def delete_category(self, category_id):
        await self.delete_one_by_id(category_id)

    def get_default(self):
        category = {
            'name': '',  # 分类名称
            'desc': '',  # 分类简介
            'icon': '',  # 分类图标url
            'privilege': 0  # 分类访问权限(所有人=0 用户=1 管理员=2)
        }
        return category
