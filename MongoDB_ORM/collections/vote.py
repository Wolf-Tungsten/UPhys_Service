from MongoDB_ORM.collections.base import CollectionBase
import pymongo

class Vote(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'vote')
        self.default = {
            'answer_id': '',
            'user_id': '',
            'vote': True,  # vote字段使用布尔值区分点赞或是踩
            'user_name': ''
        }

    async def is_up_voted(self, answer_id, user_id):
        condition = {'answer_id': answer_id, 'user_id': user_id, 'vote': True}
        counter = await self.get_count_by_condition(condition)
        if counter > 0:
            return True
        else:
            return False

    async def is_down_voted(self, answer_id, user_id):
        condition = {'answer_id': answer_id, 'user_id': user_id, 'vote': False}
        counter = await self.get_count_by_condition(condition)
        if counter > 0:
            return True
        else:
            return False

    async def get_up_vote_count(self, answer_id):
        condition = {'answer_id': answer_id, 'vote': True}
        return await self.get_count_by_condition(condition)

    async def get_down_vote_count(self, answer_id):
        condition = {'answer_id': answer_id, 'vote': False}
        return await self.get_count_by_condition(condition)

    async def get_up_vote_list(self, answer_id):
        condition = {'answer_id': answer_id, 'vote': True}
        return await self.find_by_condition(condition)

    async def get_down_vote_list(self, answer_id):
        condition = {'answer_id': answer_id, 'vote': False}
        return await self.find_by_condition(condition)

    async def up_vote(self, answer_id, user_id):
        condition = {'answer_id': answer_id, 'user_id': user_id, 'vote': False}
        await self.delete_by_condition(condition)
        condition = {'answer_id': answer_id, 'user_id': user_id, 'vote': True}
        count = await self.get_count_by_condition(condition)
        if count >= 1:
            await self.cancel_vote(answer_id, user_id)
            return False
        else:
            new_doc = self.get_default()
            new_doc['user_id'] = user_id
            new_doc['answer_id'] = answer_id
            user_info = await self.user_info(user_id)
            new_doc['user_name'] = user_info['name']
            await self.insert_one(new_doc)
            current_upvote = await self.get_up_vote_count(answer_id)
            current_downvote = await self.get_down_vote_count(answer_id)
            condition = {'_id':self.ObjectId(answer_id)}
            set = {'$set':{'vote_number':current_upvote-current_downvote}}
            await self.db['answer'].update_one(condition, set)
            return True

    async def cancel_vote(self, answer_id, user_id):
        condition = {'answer_id': answer_id, 'user_id': user_id}
        await self.delete_by_condition(condition)
        condition = {'_id': self.ObjectId(answer_id)}
        current_upvote = await self.get_up_vote_count(answer_id)
        current_downvote = await self.get_down_vote_count(answer_id)
        set = {'$set': {'vote_number': current_upvote - current_downvote}}
        await self.db['answer'].update_one(condition, set)

    async def down_vote(self, answer_id, user_id):
        condition = {'answer_id': answer_id, 'user_id': user_id, 'vote': True}
        await self.delete_by_condition(condition)
        condition = {'answer_id': answer_id, 'user_id': user_id, 'vote': False}
        count = await self.get_count_by_condition(condition)
        if count >= 1:
            await self.cancel_vote(answer_id, user_id)
            return False
        else:
            new_doc = self.get_default()
            new_doc['user_id'] = user_id
            new_doc['answer_id'] = answer_id
            user_info = await self.user_info(user_id)
            new_doc['user_name'] = user_info['name']
            new_doc['vote'] = False
            await self.insert_one(new_doc)
            current_upvote = await self.get_up_vote_count(answer_id)
            current_downvote = await self.get_down_vote_count(answer_id)
            condition = {'_id': self.ObjectId(answer_id)}
            set = {'$set': {'vote_number': current_upvote - current_downvote}}
            await self.db['answer'].update_one(condition, set)
            return True






