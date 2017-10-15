from tornado.web import RequestHandler
from handler.config import *
from handler.exceptions import ArgsError
import json

class BaseHandler(RequestHandler):

    #获取权限
    async def get_privilege(self,token):
        user=await self.db.user.get_user(token)
        if not user:
            return no_privilege
        if user['isAdmin']:
            return admin_privilege
        return user_privilege

    #鉴定管理员
    async def is_admin(self,token):
        privilege=await self.get_privilege(token=token)
        if privilege == admin_privilege:
            return True
        return False

    def finish_success(self, **kwargs):
        rs = {
            'status': 'success',
            'code':'0',
            'result':list(kwargs.values())[0]
        }
        self.finish(json.dumps(rs))

    def finish_err(self, **kwargs):
        rs = {
            'status': 'success',
            'code':'0',
            'result':list(kwargs.values())[0]
        }
        self.finish(json.dumps(rs))

    @property
    def json_body(self):
        if not hasattr(self, '_json_body'):
            if hasattr(self.request, "body"):
                try:
                    self._json_body = json.loads(self.request.body.decode('utf-8'))
                except ValueError:
                    raise ArgsError("参数不是json格式！")
        return self._json_body

    @property
    def token(self):
        return self.get_cookie("token",default='')

    @property
    def db(self):
        return self.settings['orm']