from tornado.web import RequestHandler
from handler.config import *

class BaseHandler(RequestHandler):

    #鉴定用户
    async def get_privilege(self,token):
        user=self.db.user.get_user(token)
        if user['admin']:
            return admin_privilege
        if user:
            return user_privilege
        return no_privilege


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