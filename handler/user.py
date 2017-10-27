from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError,AuthError
from tornado.httpclient import AsyncHTTPClient,HTTPRequest,HTTPError
from handler.config import CONNECT_TIME_OUT,AUTH_URL,USER_URL
import urllib.parse
import json

class UserHandler(BaseHandler):

    """
    @api {get} /user/ 获取用户信息
    @apiName GetUser
    @apiGroup User
    
    @apiSuccess {String} token 用户唯一身份令牌
    @apiSuccess {String} cardnum 一卡通号码
    @apiSuccess {Bool} isAdmin 是否是管理员
    @apiSuccess {Int} exp 问答经验值
    @apiSuccess {Int} right_num 累计答对题数
    @apiSuccess {Int} wrong_num 累计答错题数
    @apiSuccess {Int} scores 答题积分
    
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "status": "success",
        "code": "200",
        "result": {
            "token": [身份令牌],
            "cardnum": "21316xxxx",
            "isAdmin": false,
            "exp": 1000,
            "right_num": 100,
            "wrong_num": 10,
            "scores": 2000
        }
    }
    """
    async def get(self):
        my_id = await self.user_id
        user_id = self.get_argument("user_id", default=my_id)
        result = await self.db.user.get_user_with_id(user_id)
        if result is None:
            raise AuthError('用户身份信息不存在')
        self.finish_success(result=result)

    """
    @api {post} /user/ 用户登录
    @apiName AddUser
    @apiGroup User

    @apiParam {String} cardnum 一卡通号码
    @apiParam {String} password 统一身份认证密码
    
    @apiDescription 对于没有注册的新用户|cookie没有存储token的用户，调用此接口进行信息注册|获取token

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "status": "success",
        "code": "200",
        "result": "ok"
    }
    
    @apiError Error 401 AuthError 身份认证失败或获取用户名失败
    
    """
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

    """
    @api {put} /user/ 修改姓名|权限
    @apiName UpdateUser
    @apiGroup User

    @apiParam {String} name 管理员修改自己的姓名
    @apiParam {String} user_id 被修改权限的用户id
    @apiParam {Bool} isAdmin 被修改用户权限状态
    
    @apiPermission admin

    @apiDescription 请求仅限管理员操作，用于管理员修改自己的显示姓名（普通用户的姓名由统一认证接口获取真实姓名，不能修改），或者管理员修改其他用户权限。
    @apiDescription name参数较权限参数优先级高，如果存在name参数则只修改姓名，不修改权限。

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "status": "success",
        "code": "200",
        "result": "ok"
    }

    @apiError Error 401 AuthError 身份认证失败
    @apiError Error 403 PermissionDeniedError 非管理员进行操作

    """
    async def put(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        name = self.get_argument("name", None)
        if name:
            await self.db.user.put_user_with_name(self.token, name)
        else:
            user_id = self.get_argument("user_id")
            isAdmin = self.get_argument("isAdmin") == str(True)
            await self.db.user.put_user_with_id_admin(user_id, isAdmin)
        self.finish_success(result='ok')

    """
    @api {delete} /user/ 删除用户信息
    @apiName DeleteUser
    @apiGroup User
    
    @apiParam {String} user_id 将要删除的用户id

    @apiPermission admin

    @apiDescription 管理员删除用户

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "status": "success",
        "code": "200",
        "result": "ok"
    }

    @apiError Error 401 AuthError 身份认证失败
    @apiError Error 403 PermissionDeniedError 非管理员进行操作

    """
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
        data = {
            'uuid':uuid
        }
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
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