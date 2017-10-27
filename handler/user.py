from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError,AuthError
from tornado.httpclient import AsyncHTTPClient,HTTPRequest,HTTPError
from handler.config import CONNECT_TIME_OUT,AUTH_URL,USER_URL
import urllib.parse
import json

class UserHandler(BaseHandler):
    async def get(self):
        my_id = await self.user_id
        user_id = self.get_argument("user_id",default=my_id)
        result = await self.db.user.get_user_with_id(user_id)
        self.finish_success(result=result)

    async def post(self):
        cardnum = self.get_argument("cardnum")
        password = self.get_argument("password")
        uuid = await self.check_password(cardnum,password)
        user = await self.db.user.query_user_by_cardnum(cardnum)
        if not user:
            name = await self.get_name(uuid)
            token = await self.db.user.create_new_user(cardnum,name)
        else:
            token = user['token']
        self.set_cookie("token",token)
        self.finish_success(result={'token':token})

    async def put(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        name = self.get_argument("name", None)
        if name:
            await self.db.user.put_user_with_name(self.token, name)
        else:
            user_id = self.get_argument("user_id")
            isAdmin = self.get_argument("isAdmin") == str(True)
            await self.db.user.put_user_with_id_admin(user_id,isAdmin)
        self.finish_success(result='ok')

    async def delete(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        user_id = self.get_argument("user_id")
        my_id = await self.user_id
        if user_id != str(my_id):
            await self.db.user.delete_user(user_id)
        self.finish_success(result='ok')

    async def check_password(self,cardnum,password):
        data = {
            'user': cardnum,
            'password': password,
            'appid' : '9f9ce5c3605178daadc2d85ce9f8e064'
        }
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                AUTH_URL,
                method='POST',
                body=urllib.parse.urlencode(data),
                request_timeout=CONNECT_TIME_OUT)
            response = await client.fetch(request)
            response = response.body
            return response
        except HTTPError:
            raise AuthError("统一认证失败")


    async def get_name(self,uuid):
        data={
            'uuid':uuid
        }
        try:
            client = AsyncHTTPClient()
            request= HTTPRequest(
            USER_URL,
            method='POST',
            body=urllib.parse.urlencode(data),
            request_timeout=CONNECT_TIME_OUT)
            response = await client.fetch(request)
            response = json.loads(response.body.decode('utf-8'))
            return response['content']['name']
        except HTTPError:
            raise AuthError("未能获取用户名")


routes.handlers +=[
    (r'/user',UserHandler),
]