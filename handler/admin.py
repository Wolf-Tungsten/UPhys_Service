from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError, ResourceNotExistError

class AdminHandler(BaseHandler):

    """
        @api {get} /admin 核查超级管理员状态
        @apiName CheckSuperAdmin
        @apiGroup Admin

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": "ok"
        }

    """
    async def get(self):
        await self.db.user.check_super_admin()
        self.finish_success(result='ok')

    """
        @api {post} /admin 管理员创建用户
        @apiName AdminCreateUser
        @apiGroup Admin

        @apiParam {String} cardnum 一卡通号码
        @apiParam {String} password 密码
        @apiParam {String} name 用户姓名
        @apiParam {bool} isAdmin 是否管理员
        @apiParam {bool} isSuperAdmin 是否超级管理员


        @apiParamExample {json} Request-Example:
            {
                "cardnum": 一卡通号码,
                "password": 密码明文,
                "name": 用户姓名,
                "isAdmin": True
                
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": "ok"
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def post(self):
        cardnum = self.get_argument('cardnum')
        password = self.get_argument('password')
        name = self.get_argument('name')
        isAdmin = self.get_argument('isAdmin')
        if isAdmin:
            if await self.is_super_admin:
                await self.db.user.admin_create_new_user(cardnum, password, name, isAdmin=True)
                self.finish_success(result='ok')
            else:
                raise PermissionDeniedError('只允许超级管理员创建管理员用户')
        else:
            if await self.is_admin:
                await self.db.user.admin_create_new_user(cardnum, password, name, isAdmin=False)
                self.finish_success(result='ok')
            else:
                raise PermissionDeniedError('只允许管理员创建普通用户')

    """
        @api {put} /admin 超级管理员设置管理员（对已存在用户）
        @apiName AdminSetAdmin
        @apiGroup Admin

        @apiParam {String} cardnum 一卡通号码


        @apiParamExample {json} Request-Example:
            {
                "cardnum": 一卡通号码
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": "ok"
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def put(self):
        if not await self.is_super_admin:
            raise PermissionDeniedError("需要超级管理员权限")
        cardnum = self.get_argument("cardnum")
        await self.db.user.set_admin(cardnum)
        self.finish_success(result='ok')

    """
        @api {delete} /admin 超级管理员取消管理员身份
        @apiName AdminCancelAdmin
        @apiGroup Admin

        @apiParam {String} cardnum 一卡通号码


        @apiParamExample {json} Request-Example:
            {
                "cardnum": 一卡通号码
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": "ok"
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def delete(self):
        if not await self.is_super_admin:
            raise PermissionDeniedError("需要管理员权限")
        cardnum = self.get_argument("cardnum")
        await self.db.user.cancel_admin(cardnum)
        self.finish_success(result='ok')

routes.handlers += [
    (r'/admin', AdminHandler),
]