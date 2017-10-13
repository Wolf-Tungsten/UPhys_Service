from .MongoDB import base


class MongodbORM(object):
    def __init__(self, mongodb):
        control = base.MongodbControl(mongodb)
        self.db_control = control
        self.base = control

        # 下面添加各个数据表
