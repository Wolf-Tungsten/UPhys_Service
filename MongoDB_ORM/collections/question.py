from MongoDB_ORM.collections.base import CollectionBase
import pymongo

class Question(CollectionBase):
    def __init__(self, db):
        CollectionBase(self, db, 'question')

    # GET /questions
    def get_questions(self, category_id, page, pagesize):
        condition = {'category_id': category_id}
        limit = pagesize
        skip = (page - 1) * pagesize
        sort = [('post_time', pymongo.DESCENDING)]
        cursor = self.collection.find(condition, limit=limit, skip=skip, sort=sort)
        return cursor

    # GET /question
    async def get_question(self, question_id):
        return await self.find_one_by_id(question_id)

    # POST /question
    async def post_question(self, category_id, question):
        question['category_id'] = category_id
        await self.insert_one(question)

    # PUT /question
    async def put_question(self, question_id, question):
        await self.update_one_by_id(question_id, question)

    # DELETE /question
    async def delete_question(self, question_id):
        await self.delete_one_by_id(question_id)

    def get_default(self):
        question = {
            'title': '',  # 问题标题
            'content': '',  # 问题内容
            'images': [],  # 问题所包含图片url列表
            'read_num': 0,  # 问题阅读量
            'user_id': '',  # 问题发布者
            'post_time': 0.0,  # 问题发布时间
            'modify_user_id': '',  # 问题最后修改者
            'modify_time': 0.0  # 问题最后修改时间
        }
        return question
