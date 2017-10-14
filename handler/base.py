from tornado.web import RequestHandler
from handler.config import *
import json

class BaseHandler(RequestHandler):

    #鉴定用户
    async def get_privilege(self,token):
        user=self.db.user.get_user(token)
        if user['admin']:
            return admin_privilege
        if user:
            return user_privilege
        return no_privilege

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

    '''
    async def is_user(self,token):
        user=self.db.user.get_user(token=token)
        if user:
            return True
        return False


    #鉴定管理员
    async def is_admin(self,token):
        admin=await self.db.user.get_user(token=token)
        if admin['isAdmin']:
                return True
        return False
    '''
    @property
    def db(self):
        return self.settings['orm']