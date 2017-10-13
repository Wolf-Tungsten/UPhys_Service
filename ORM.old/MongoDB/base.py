# coding=utf-8
import bson
import copy
import pymongo


def ObjectId(id):
    return bson.objectid.ObjectId(id)


class MongodbOrmBase(object):
    def __init__(self, mongodb_control):
        self.db = mongodb_control


class MongodbControl(object):
    def __init__(self, mongo_client):
        self.db = mongo_client

    def ObjectId(id):
        return bson.objectid.ObjectId(id)

    # To match dict_src to dict_dst(like 'right join' in sql)
    def dict_match(self, dict_src, dict_default, default=None):
        for i in dict_src:
            if i in dict_default:
                dict_default[i] = dict_src[i]
        for i in dict_default:
            if dict_default[i] == default:
                return None;
        return dict_default

    # get one document
    async def get_document_one(self, condition, colName):
        document = await self.db[colName].find_one(condition)
        return document

    # get count of documents
    async def get_document_count(self, condition, colName):
        n = await self.db[colName].find(condition).count()
        return n

    # get document List by condition, sortby, sort, limit, skip
    async def get_document_list(self, condition, sortby, sort, limit, skip, colName):
        sortlist = {
            '+': pymongo.ASCENDING,
            '-': pymongo.DESCENDING
        }
        cursor = self.db[colName].find(condition)
        cursor.sort(sortby, sortlist[sort]).limit(limit).skip(skip)
        documentlist = []
        async for document in cursor:
            documentlist.append(document)
        return documentlist

    # update document
    async def update(self, condition, document, colName):
        await self.db[colName].update(condition, document)

    # insert doucumnet
    async def insert(self, document, colName):
        result = await self.db[colName].insert(document)
        return result

    # delete document
    async def delete(self, condition, colName):
        await self.db[colName].delete_many(condition)

    # update document by id
    async def update_by_id(self, document_id, document):


    def get_category_default(self):
        category = {
            'name': '',  # 分类名称
            'desc': '',  # 分类简介
            'icon': '',  # 分类图标url
            'privilege': 0  # 分类访问权限(所有人=0 用户=1 管理员=2)
        }
        return category

    def get_question_default(self):
        question = {
            'title': '',  # 问题标题
            'content': '',  # 问题内容
            'images': [],  # 问题所包含图片url列表
            'category_id': '',  # 问题所在分类
            'read_num': 0,  # 问题阅读量
            'user_id': '',  # 问题发布者
            'post_time': 0.0,  # 问题发布时间
            'modify_user_id': '',  # 问题最后修改者
            'modify_time': 0.0  # 问题最后修改时间
        }
        return question

    def get_answer_default(self):
        answer = {
            'title': '',  # 回答标题
            'content': '',  # 回答内容
            'images': '',  # 回答包含图片url列表
            'question_id': '',  # 回答所属问题id
            'likes': [],  # 回答支持者id列表

        }
        return answer

    def get_column_default(self):
        column = {
            'name': '',  # 专栏名称
            'desc': '',  # 专栏简介
            'icon': '',  # 专栏图标url
            'privilege': '',  # 专栏访问权限(所有人=0 用户=1 管理员=2)
            'visible': False  # 是否显示在专栏列表中，某些专栏只在微信中有入口，在专栏列表中不显示(bool)
        }
        return column

    def get_article_default(self):
        article = {
            'title': '',  # 文章标题
            'content': '',  # 文章内容
            'videos': [],  # 文章附带视频url列表
            'images': [],  # 文章附带图片url列表
            'column_id': '',  # 文章所属专栏
            'read_num': 0,  # 文章阅读量
            'like_num': 0,  # 文章点赞数
            'user_id': '',  # 文章发布者
            'post_time': 0.0,  #文章发布时间
            'privilege': ''  # 文章阅读权限(所有人=0 用户=1 管理员=2)
        }
        return article

    def get_chapter_default(self):
        chapter = {
            'title': '',  # 章节名
            'privilege': ''  # 章节自测权限(所有人=0 用户=1 管理员=2)
        }
        return chapter

    def get_puzzle_default(self):
        puzzle = {
            'number': '',  # 题号（字符串）
            'content': '',  # 题目内容
            'images': '',  # 题目包含图片url列表
            'type': '',  # 题型(单选='single' 多选='multiple')
            'chapter_id': '',  # 所属章节
            'choices': [],  # 选项列表（字符串列表）
            'answer': [],  # 正确答案选项列表（下标列表）
            'scores': 0,  # 题目积分数
            'right_num': 0,  # 被回答正确次数
            'wrong_num': 0  # 被回答错误次数
        }
        return puzzle

    def get_user_default(self):
        user = {
            'token': '',  # 认证token
            'cardnum': '',  # 一卡通号
            'name': '',  # 姓名
            'isAdmin': False,  # 是否管理员
            'exp': 0,  # 问答经验值
            'right_num': 0,  # 累计答对题数
            'wrong_num': 0,  # 累计答错题数
            'scores': 0  # 答题积分
        }
