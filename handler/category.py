from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError
import IPython

class sCategoryHandler(BaseHandler):
    async def get(self):
        privilege = await self.privilege
        list = await self.db.category.get_categories(privilege)
        self.finish_success(result=list)

class CategoryHandler(BaseHandler):
    async def get(self):
        category_id = self.get_argument("category_id")
        privilege = await self.privilege
        list = await self.db.category.get_category(category_id,privilege)
        question_count = await self.db.question.get_question_count(category_id)
        if list:
            list.update({"question_count":question_count})
        self.finish_success(result=list)

    async def post(self):
        if  not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        category = self.get_argument("category")
        default_category = self.db.category.get_default()
        for c in category:
            default_category[c] = category[c]
        await self.db.category.post_category(default_category)
        self.finish_success(result='ok')

    async def put(self):
        if  not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        category_id = self.get_argument("category_id")
        category = self.get_argument("category")
        await self.db.category.put_category(category_id,category)
        self.finish_success(result='ok')


    async def delete(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        category_id = self.get_argument("category_id")
        await self.db.category.delete_category(category_id)
        self.finish_success(result='ok')

routes.handlers +=[
    (r'/categories',sCategoryHandler),
    (r'/category',CategoryHandler)
]