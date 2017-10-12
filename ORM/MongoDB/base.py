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

    # @token ----------------------------------------
    # be used to identity user
    def get_token_default(self):
        token = {
            'userId': '',
            'accessToken': '',
            'accessTime': ''
        }
        return token

    def brief_token(self, document, type='brief'):
        if type == 'brief':
            brief_document = {
                'userId': '',
                'accessToken': '',
                'accessTime': ''
            }
            r_document = self.dict_match(document, brief_document)
        return r_document

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