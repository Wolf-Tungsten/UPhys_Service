from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError

class sQuestionHandler(BaseHandler):
    """
        @api {get} /questions/ 获取分类下题目
        @apiName GetAllQuestion
        @apiGroup Question
        
        @apiParam {String} category_id 检索问题所在目录id
        @apiParam {Int} page 分页
        @apiParam {Int} pagesize 每页显示问题数
        @apiParamExample {json} Request-Example:
            {
                "category_id": [分类id],
                "page": [分页],
                "pagesize": [每页尺寸]
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": [{
                'title': '',  # 问题标题
                'content': '',  # 问题内容
                'images': [],  # 问题所包含图片url列表
                'read_num': 0,  # 问题阅读量
                'user_id': '',  # 问题发布者
                'post_time': 0.0,  # 问题发布时间
                'modify_user_id': '',  # 问题最后修改者
                'modify_time': 0.0,  # 问题最后修改时间
                'category_id': ''  # 问题所在category_id
            },
            {
                'title': '',  # 问题标题
                'content': '',  # 问题内容
                'images': [],  # 问题所包含图片url列表
                'read_num': 0,  # 问题阅读量
                'user_id': '',  # 问题发布者
                'post_time': 0.0,  # 问题发布时间
                'modify_user_id': '',  # 问题最后修改者
                'modify_time': 0.0,  # 问题最后修改时间
                'category_id': ''  # 问题所在category_id
            }]
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def get(self):
        category_id = self.get_argument("category_id")
        page = self.get_argument("page")
        pagesize = self.get_argument("pagesize")
        privilege = await self.privilege
        question_privilege = await self.db.category.get_privilege(category_id)
        if question_privilege > privilege:
            raise PermissionDeniedError("没有访问权限")
        list = await self.db.question.get_questions(category_id,page,pagesize)
        self.finish_success(result=list)

class QuestionHandler(BaseHandler):
    """
        @api {get} /question/ 根据id获取题目
        @apiName GetQuestion
        @apiGroup Question

        @apiParam {String} question_id 问题id
        @apiParamExample {json} Request-Example:
            {
                "question_id": [问题id]
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": {
                'title': '',  # 问题标题
                'content': '',  # 问题内容
                'images': [],  # 问题所包含图片url列表
                'read_num': 0,  # 问题阅读量
                'user_id': '',  # 问题发布者
                'post_time': 0.0,  # 问题发布时间
                'modify_user_id': '',  # 问题最后修改者
                'modify_time': 0.0,  # 问题最后修改时间
                'category_id': '',  # 问题所在category_id
                'answer_count':0 # 当前问题的答案数量
            }
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def get(self):
        if not await self.question_allow:
            raise PermissionDeniedError("没有访问权限")
        question_id = self.get_argument("question_id")
        list = await self.db.question.get_question(question_id)
        answer_count = await self.db.answer.get_answer_count(question_id)
        list.update({"answer_count": answer_count})
        self.finish_success(result=list)
    """
        @api {post} /question/ 添加题目
        @apiName AddQuestion
        @apiGroup Question

        @apiParam {String} category_id 所添加题目所在分类id
        @apiParam {json} question 所添加问题的内容
        @apiParamExample {json} Request-Example:
            {
                "category_id":[分类id],
                "question":{
                    'title': '',  # 问题标题
                    'content': '',  # 问题内容
                    'images': [],  # 问题所包含图片url列表
                    'category_id': ''  # 问题所在category_id            
                }
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
        user_id =await self.user_id
        privilege = await self.privilege
        category_id = self.get_argument("category_id")
        question_privilege = await self.db.category.get_privilege(category_id)
        if question_privilege > privilege:
            raise PermissionDeniedError("没有访问权限")
        default_question = self.db.question.get_default()
        question = self.get_argument("question")
        for q in question:
            default_question[q] = question[q]
        await self.db.question.post_question(category_id, default_question, user_id)
        await self.db.user.change_exp(user_id, 10)
        self.finish_success(result='ok')
    """
        @api {put} /question/ 修改题目
        @apiName ModifyQuestion
        @apiGroup Question

        @apiParam {String} question_id 所修改问题的id
        @apiParam {json} question 所修改问题的内容
        @apiParamExample {json} Request-Example:
            {
                "question_id":[问题id],
                "question":{
                    'title': '',  # 问题标题
                    'content': '',  # 问题内容
                    'images': [],  # 问题所包含图片url列表
                    'category_id': ''  # 问题所在category_id            
                }
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": "ok"
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有修改权限

    """
    async def put(self):
        modify_user_id = await self.user_id
        question_id = self.get_argument("question_id")
        user_id = await self.db.question.get_user_id(question_id)
        if not await self.is_admin and modify_user_id != user_id:
            raise PermissionDeniedError("没有修改权限")
        question = self.get_argument("question")
        await self.db.question.put_question(question_id, question, modify_user_id)
        self.finish_success(result='ok')

    """
        @api {delete} /question/ 删除题目
        @apiName DeleteQuestion
        @apiGroup Question
        @apiPermission admin
        @apiParam {String} question_id 删除问题的id
        @apiParamExample {json} Request-Example:
            {
                "question_id":[问题id]
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": "ok"
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有修改权限

    """
    async def delete(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        question_id = self.get_argument("question_id")
        user_id = await self.db.question.get_user_id(question_id)
        await self.db.question.delete_question(question_id)
        await self.db.user.change_exp(user_id,-10)
        self.finish_success(result='ok')

routes.handlers += [
    (r'/questions',sQuestionHandler),
    (r'/question',QuestionHandler)
]