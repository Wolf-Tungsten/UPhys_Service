from handler.base import BaseHandler

class CategoryHandler(BaseHandler):
    def get(self):
        token=self.get_argument("token",default=None)
        privilege=self.get_privilege(token)
        list=self.db.category.get_categories(privilege)
        self.finish