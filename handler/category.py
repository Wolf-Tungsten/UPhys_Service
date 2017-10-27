from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError,ResourceNotExistError
import IPython

class sCategoryHandler(BaseHandler):
    """
        @api {get} /categories 获取所有目录
        @apiName GetAllCategory
        @apiGroup Category
        
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": [{
                "_id": id, # 分类id
                "name": "光学",  # 分类名称
                "desc": "关于光学的分类",  # 分类简介
                "icon": "https://.../",  # 分类图标url
                "privilege": 0  # 分类访问权限(所有人=0 用户=1 管理员=2)
            },
            {
                "_id": id, # 分类id
                "name": "振动",  # 分类名称
                "desc": "振动专题",  # 分类简介
                "icon": "https://.../",  # 分类图标url
                "privilege": 0  # 分类访问权限(所有人=0 用户=1 管理员=2)
            }]
        }

        @apiError 401-AuthError 身份认证失败

    """
    async def get(self):
        privilege = await self.privilege
        list = await self.db.category.get_categories(privilege)
        self.finish_success(result=list)

class CategoryHandler(BaseHandler):
    """
        @api {get} /category 获取目录信息
        @apiName GetCategory
        @apiGroup Category
        @apiParamExample {json} Request-Example:
            {
                "category_id":"1ad124bbf42"
            }
        @apiParam {String} category_id 待检索目录id
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result":{
                "_id": id, # 分类id
                "name": "振动",  # 分类名称
                "desc": "振动专题",  # 分类简介
                "icon": "https://.../",  # 分类图标url
                "privilege": 0  # 分类访问权限(所有人=0 用户=1 管理员=2)
                "question_count": 10 # 该分类下问题数目
                
            }
        }
        @apiError 401-AuthError 身份认证失败
        @apiError 404-ResourceNotExistError category_id不存在
    """
    async def get(self):
        category_id = self.get_argument("category_id")
        privilege = await self.privilege
        result = await self.db.category.get_category(category_id, privilege)
        question_count = await self.db.question.get_question_count(category_id)
        if result is not None:
            result.update({"question_count": question_count})
        else:
            raise ResourceNotExistError('没有对应id的目录')
        self.finish_success(result=result)

    """
        @api {post} /category 添加一个目录
        @apiName AddCategory
        @apiGroup Category
    
        @apiPermission admin
        @apiParam {String} name 分类名称
        @apiParam {String} desc 分类简介
        @apiParam {String} icon 分类图标url
        @apiParam {Int} privilege 分类权限
        @apiParamExample {json} Request-Example:
            {
                "name":"光学",
                "desc":"光学相关习题",
                "icon":[url],
                "privilege":1
            }
        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 需要管理员权限
    """
    async def post(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        category = self.get_argument("category")
        default_category = self.db.category.get_default()
        for c in category:
            default_category[c] = category[c]
        await self.db.category.post_category(default_category)
        self.finish_success(result='ok')

    """
        @api {put} /category 修改目录信息
        @apiName EditCategory
        @apiGroup Category

        @apiPermission admin
        @apiParam {String} category_id 分类id
        @apiParam {json} category 修改信息
        @apiParamExample {json} Request-Example:
            {
                "category_id":[category_id],
                "category":{
                    "name":"光学",
                    "desc":"光学相关习题",
                    "icon":[url],
                    "privilege":1
                    }
            }        
        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 需要管理员权限
    """
    async def put(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        category_id = self.get_argument("category_id")
        category = self.get_argument("category")
        await self.db.category.put_category(category_id,category)
        self.finish_success(result='ok')

    """
        @api {delete} /category 删除目录信息
        @apiName DeleteCategory
        @apiGroup Category

        @apiPermission admin
        @apiParam {String} category_id 分类id
        @apiParamExample {json} Request-Example:
            {
                "category_id":[category_id]
            }
        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 需要管理员权限
    """
    async def delete(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        category_id = self.get_argument("category_id")
        await self.db.category.delete_category(category_id)
        self.finish_success(result='ok')

routes.handlers += [
    (r'/categories', sCategoryHandler),
    (r'/category', CategoryHandler)
]