from .collections.category import Category


class ORM(object):
    def __init__(self, db):
        self.db = db

        self.category = Category(self.db)
