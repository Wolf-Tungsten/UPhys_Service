from MongoDB_ORM.collections.base import CollectionBase
import hashlib
import datetime as dt

class User(CollectionBase):
    def __init__(self, db):
        CollectionBase(self, db, 'user')

    def get_default(self):
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
        return user

    # 创建新用户
    # 身份认证通过，但是get_user_by_cardnum为None时调用创建新用户
    async def create_new_user(self, cardnum, name, isAdmin=False):
        token_str = cardnum + str(dt.datetime.now().timestamp())
        sha256 = hashlib.sha256()
        sha256.update(token_str.encode('utf8'))
        token = sha256.hexdigest()
        user_template = self.get_default()
        user_template['token'] = token
        user_template['cardnum'] = cardnum
        user_template['name'] = name
        user_template['isAdmin'] = isAdmin
        await self.insert_one(user_template)

    # 使用token获取用户身份
    async def query_user_by_token(self, token):
        condition = {'token': token}
        return await self.collection.find_one(condition)

    # 使用cardnum获取用户身份
    # 仅限登录验证成功后鉴定是否为新用户，其他身份验证应使用token获取
    async def query_user_by_cardnum(self, cardnum):
        condition = {'cardnum': cardnum}
        return await self.collection.find_one(condition)

    # 根据id修改用户经验值，delta可正可负
    async def change_exp(self, user_id, delta):
        current = await self.find_one_by_id(user_id)
        current['exp'] = current['exp'] + delta
        await self.update_one_by_id(user_id, current)

    # 根据id修改用户答对题数，right_num可正可负，默认为1
    async def change_right_num(self, user_id, right_num=1):
        current = await self.find_one_by_id(user_id)
        current['right_num'] = current['right_num'] + right_num
        await self.update_one_by_id(user_id, current)

    # 根据id修改用户答对错数，wrong_num可正可负，默认为1
    async def change_wrong_num(self, user_id, wrong_num=1):
        current = await self.find_one_by_id(user_id)
        current['wrong_num'] = current['wrong_num'] + wrong_num
        await self.update_one_by_id(user_id, current)

    # 根据id修改用户答题积分，delta可正可负
    async def change_score(self, user_id, delta):
        current = await self.find_one_by_id(user_id)
        current['scores'] = current['scores'] + delta
        await self.update_one_by_id(user_id, current)

    # GET /user
    async def get_user(self, token):
        return await self.query_user_by_token(token)

    # GET /user&user_id
    async def get_user_with_id(self, user_id):
        return await self.find_one_by_id(user_id)

    # PUT /user&name
    async def put_user_with_name(self, token, username):
        current = await self.query_user_by_token(token)
        current['name'] = username
        await self.update_one_by_id(str(current['_id']), current)

    # PUT /user&user_id&isAdmin
    async def put_user_with_id_admin(self, user_id, isAdmin):
        current = await self.find_one_by_id(user_id)
        current['isAdmin'] = isAdmin
        await self.update_one_by_id(user_id, current)

    # DELETE /user
    async def delete_user(self, user_id):
        await self.delete_one_by_id(user_id)


