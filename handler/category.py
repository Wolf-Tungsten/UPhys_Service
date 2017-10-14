from handler.base import BaseHandler
import routes

class CategoryHandler(BaseHandler):
    def get(self):
        token=self.get_argument("token",default=None)
        privilege=self.get_privilege(token)
        #list=self.db.category.get_categories(privilege)
        #self.finish_success(list)
        self.write(privilege)
routes.handlers+={
    r'/categories',CategoryHandler
}