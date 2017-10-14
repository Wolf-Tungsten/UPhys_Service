from handler.base import BaseHandler

class CategoryHandler(BaseHandler):
    def get(self):
        t=self.get_argument("token",default=None)
        if self.is_admin(t):
            list=self.db.category.get_categories(3)
        elif self.is_user(t):
            list=self.db.category.get_categories(2)
        list=self.db.category.get_categories(1)
        self.finish