from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError

class sAnswerHandler(BaseHandler):
    """
        @api {get} /answers 获取题目所有回答
        @apiName GetAllAnswers
        @apiGroup Answer

        @apiParam {String} question_id 问题id
        @apiParam {Int} page 分页
        @apiParam {Int} pagesize 每页显示答案数
        @apiParamExample {json} Request-Example:
            {
                "question_id": [问题id],
                "page": [分页],
                "pagesize": [每页尺寸]
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": [{
                '_id':[回答id],
                'title': '',  # 回答标题
                'content': '',  # 回答内容
                'images': '',  # 回答包含图片url列表
                'question_id': '',  # 回答所属问题id
                'likes': [],  # 回答支持者id列表
                'dislikes': [],  # 回答反对者id列表
                'user_id': '',  # 发布者user_id
                'post_time': 0.0,  # 发布时间
                'modify_user_id': '',  # 最后修改者id
                'modify_time': 0.0  # 最后修改时间
            },
            {
                '_id':[回答id],
                'title': '',  # 回答标题
                'content': '',  # 回答内容
                'images': '',  # 回答包含图片url列表
                'question_id': '',  # 回答所属问题id
                'likes': [],  # 回答支持者id列表
                'dislikes': [],  # 回答反对者id列表
                'user_id': '',  # 发布者user_id
                'post_time': 0.0,  # 发布时间
                'modify_user_id': '',  # 最后修改者id
                'modify_time': 0.0  # 最后修改时间
            }]
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def get(self):
        question_id = self.get_argument("question_id")
        page = self.get_argument("page")
        pagesize = self.get_argument("pagesize")
        if not await self.question_allow:
            raise PermissionDeniedError("没有访问权限")
        list = await self.db.answer.get_answers(question_id,page,pagesize)
        self.finish_success(result=list)

class AnswerHandler(BaseHandler):
    """
        @api {post} /answer 提交回答
        @apiName AddAnswer
        @apiGroup Answer

        @apiParam {String} question_id 问题id
        @apiParam {json} answer 回答

        @apiParamExample {json} Request-Example:
            {
                "question_id": [问题id],
                "answer":{             
                    'title': '',  # 回答标题
                    'content': '',  # 回答内容
                    'images': ''  # 回答包含图片url列表
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
        question_id = self.get_argument("question_id")
        if not await self.question_allow:
            raise PermissionDeniedError("没有访问权限")
        default_answer = self.db.answer.get_default()
        answer = self.get_argument("answer")
        for a in answer:
            default_answer[a] = answer[a]
        await self.db.answer.post_answer(question_id, default_answer, user_id)
        await self.db.user.change_exp(user_id, 20)
        self.finish_success(result='ok')
    """
        @api {put} /answer 修改回答
        @apiName ModifyAnswer
        @apiGroup Answer

        @apiParam {String} answer_id 问题id
        @apiParam {json} answer 回答

        @apiParamExample {json} Request-Example:
            {
                "answer_id": [问题id],
                "answer": {             
                    'title': '',  # 回答标题
                    'content': '',  # 回答内容
                    'images': []  # 回答包含图片url列表
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
        answer_id = self.get_argument("answer_id")
        user_id = await self.db.answer.get_user_id(answer_id)
        if  not await self.is_admin and modify_user_id != user_id:
            raise PermissionDeniedError("没有修改权限")
        answer = self.get_argument("answer")
        await self.db.answer.put_answer(answer_id,answer,modify_user_id)
        self.finish_success(result='ok')

    """
        @api {delete} /answer 删除回答
        @apiName DeleteAnswer
        @apiGroup Answer
        @apiPermission admin
        @apiParam {String} answer_id 问题id

        @apiParamExample {json} Request-Example:
            {
                "answer_id": [答案id]
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": "ok"
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 需要管理员权限

    """
    async def delete(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        answer_id = self.get_argument("answer_id")
        user_id = await self.db.answer.get_user_id(answer_id)
        await self.db.answer.delete_answer(answer_id)
        await self.db.user.change_exp(user_id,-20)
        self.finish_success(result='ok')

class VoteHandler(BaseHandler):
    """
        @api {post} /answer/vote 给答案打call
        @apiName VoteAnswer
        @apiGroup Answer

        @apiParam {String} answer_id 问题id

        @apiParamExample {json} Request-Example:
            {
                "answer_id": [答案id]
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
        user_id = await self.user_id
        answer_id = self.get_argument("answer_id")
        if not await self.answer_allow:
            raise PermissionDeniedError("没有访问权限")
        await self.db.answer.post_answer_vote(answer_id,user_id)
        user_id = await self.db.answer.get_user_id(answer_id)
        await self.db.user.change_exp(user_id,1)
        self.finish_success(result='ok')
    """
        @api {delete} /answer/vote 取消投票
        @apiName DeleteVoteAnswer
        @apiGroup Answer

        @apiParam {String} answer_id 问题id

        @apiParamExample {json} Request-Example:
            {
                "answer_id": [答案id]
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
        user_id = await self.user_id
        answer_id = self.get_argument("answer_id")
        if not await self.answer_allow:
            raise PermissionDeniedError("没有访问权限")
        await self.db.answer.delete_answer_vote(answer_id,user_id)
        user_id = await self.db.answer.get_user_id(answer_id)
        await self.db.user.change_exp(user_id,-1)
        self.finish_success(result='ok')

routes.handlers +=[
    (r'/answers',sAnswerHandler),
    (r'/answer',AnswerHandler),
    (r'/answer/vote',VoteHandler)
]