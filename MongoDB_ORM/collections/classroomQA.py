# 课堂问答ORM
from MongoDB_ORM.collections.base import CollectionBase
import pymongo
import random


class Question(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'classroom_Q_and_A_question')
        self.default = {
            "user_id": '',  # 发布问题的老师的user_id
            "question": '',  # 问题的文本内容描述
            "image_url": '',  # 问题的附件图片
            "answer": '',  # 问题的正确答案
            "post_time": '',  # 问题的发布时间
            "code": ''  # 问题的code，用于学生找到问题
        }

    async def get_all_my_questions(self, user_id, pagesize, page):
        condition = {'user_id': user_id}
        sort = [('post_time', pymongo.DESCENDING)]
        result = await self.find_pages_by_condition(condition, sort=sort, pagesize=pagesize, page=page)
        return result

    async def get_a_question_by_code(self, code):
        condition = {'code': code}
        return await self.find_by_condition(condition)

    async def put_up_a_question(self, user_id, question, image_url, answer):
        # 生成6位问题code
        code = ''
        for i in range(6):
            code = code + random.choice('1234567890')
        template = self.get_default()
        template['user_id'] = user_id
        template['question'] = question
        template['image_url'] = image_url
        template['answer'] = str(answer)
        template['post_time'] = self.timestamp()
        template['code'] = code
        await self.insert_one(template)
        return code

    async def modify_a_question(self, question_id, **kwargs):
        old_question = await self.find_one_by_id(question_id)
        for (k, v) in kwargs:
            old_question[k] = v
        old_question['post_time'] = self.timestamp()
        await self.update_one_by_id(question_id, old_question)

    async def delete_a_question(self, question_id):
        await self.delete_one_by_id(question_id)


class Answer(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'classroom_Q_and_A_answer')
        self.default = {
            "student_id": '',  # 回答问题的同学id
            "question_id": '',  # 回答的问题id
            "answer": '',  # 学生答案
            "is_correct": False,  # 是否正确
            "post_time": '',  # 问题回答的时间
        }

    async def answer_a_question(self, student_id, question_id, answer):
        question = await self.find_one_by_id(question_id)
        is_correct = question['answer'] == str(answer)
        template = self.get_default()
        template['student_id'] = student_id
        template['question_id'] = question_id
        template['answer'] = str(answer)
        template['is_correct'] = is_correct
        template['post_time'] = self.timestamp()
        await self.insert_one(template)

    async def get_answers_of_a_student(self, student_id, pagesize, page):
        sort = [('post_time', pymongo.DESCENDING)]
        condition = {'student_id': student_id}
        return await self.find_pages_by_condition(condition, sort=sort, pagesize=pagesize, page=page)

    async def get_answers_of_a_question(self, question_id, pagesize, page):
        sort = [('post_time', pymongo.DESCENDING)]
        condition = {'question_id': question_id}
        return await self.find_pages_by_condition(condition, sort=sort, pagesize=pagesize, page=page)
