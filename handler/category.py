from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError,MissingArgumentError
import IPython

class sCategoryHandler(BaseHandler):
    async def get(self):
        token = self.token
        privilege = await self.get_privilege(token=token)
        list = await self.db.category.get_categories(privilege)
        self.finish_success(result=list)

class CategoryHandler(BaseHandler):
    async def get(self):
        token = self.token
        json = self.json_body
        try:
            category_id = json["category_id"]
        except KeyError:
            raise MissingArgumentError("缺少category_id")
        privilege = await self.get_privilege(token)
        list = await self.db.category.get_category(category_id,privilege)
        self.finish_success(result=list)

    async def post(self):
        token = self.token
        json = self.json_body
        if  not await self.is_admin(token):
            raise PermissionDeniedError("需要管理员权限")
        try:
            category = json['category']
        except KeyError:
            raise MissingArgumentError("缺少category")
        await self.db.category.post_category(category)
        self.finish_success(result='ok')

    async def put(self):
        token = self.token
        json = self.json_body
        if  not await self.is_admin(token):
            raise PermissionDeniedError("需要管理员权限")
        try:
            category_id = json['category_id']
            category = json['category']
        except KeyError:
            raise MissingArgumentError("缺少参数")
        await self.db.category.put_category(category_id,category)
        self.finish_success(result='ok')


    async def delete(self):
        token = self.token
        json = self.json_body
        if not await self.is_admin(token):
            raise PermissionDeniedError("需要管理员权限")
        try:
            category_id = json['category_id']
        except KeyError:
            raise MissingArgumentError("缺少category_id")
        await self.db.category.delete_category(category_id)
        self.finish_success(result='ok')

routes.handlers +=[
    (r'/categories',sCategoryHandler),
    (r'/category',CategoryHandler)
]