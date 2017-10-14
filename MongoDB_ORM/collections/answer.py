from MongoDB_ORM.collections.base import CollectionBase


class Answer(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'answer')

    # GET /answers
    async def get_answers(self, question_id, page, pagesize):
        condition = {'question_id': question_id}
        sort = [('post_time',self.DESCENDING)]
        return await self.find_pages_by_condition(condition, sort, page, pagesize)

    # POST /answer
    async def post_answer(self, answer, user_id):
        answer['user_id'] = user_id
        answer['post_time'] = self.timestamp()
        await self.insert_one(answer)

    # PUT /answer
    async def put_answer(self, answer_id, answer, user_id):
        answer['modify_user_id'] = user_id
        answer['modify_time'] = self.timestamp()
        await self.update_one_by_id(answer_id, answer)

    # DELETE /answer
    async def delete_answer(self, answer_id):
        await self.delete_one_by_id(answer_id)

    # POST /answer/vote
    async def post_answer_vote(self, answer_id, user_id):
        current_answer = await self.find_one_by_id(answer_id)
        if user_id not in current_answer['likes']:
            current_answer['likes'].append(user_id)
        if user_id in current_answer['dislikes']:
            index = current_answer['dislikes'].index(user_id)
            current_answer['dislikes'].remove(index)
        await self.update_one_by_id(answer_id, current_answer)

    # DELETE /answer/vote
    async def delete_answer_post(self, answer_id, user_id):
        current_answer = await self.find_one_by_id(answer_id)
        if user_id not in current_answer['dislikes']:
            current_answer['dislikes'].append(user_id)
        if user_id in current_answer['likes']:
            index = current_answer['likes'].index(user_id)
            current_answer['likes'].remove(index)
        await self.update_one_by_id(answer_id, current_answer)

    def get_default(self):
        answer = {
                'title': '',  # 回答标题
                'content': '',  # 回答内容
                'images': '',  # 回答包含图片url列表
                'question_id': '',  # 回答所属问题id
                'likes': [],  # 回答支持者id列表
                'dislikes': [],  # 回答反对者id列表
                'user_id': '',  # 发布者user_id
                'post_time': 0.0,  # 发布时间
                'modify_user_id': '',  # 最后修改者id
                'modify_time': 0.0  # 最后修改时间
        }
        return answer
