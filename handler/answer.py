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
        "result": {
            "_id": "5a0cd7d2ee3cf828eedcb7c4",
            "title": "",
            "content": "穿了！",
            "images": [],
            "question_id": "5a0b0acbee3cf80f6f0c9212",
            "likes": [
                "5a09d175ee3cf8026b9edfe8"
            ],
            "dislikes": [
                "5a08f22a7c193b2fef2cb63d"
            ],
            "user_id": "5a09dxxxxx",
            "post_time": 1510791122,
            "modify_user_id": "",
            "modify_time": 1510791122,
            "user_name": "高睿昊",
            "upvote_count": 0,
            "downvote_count": 1
        }
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def get(self):
        question_id = self.get_argument("question_id")
        page = int(self.get_argument("page"))
        pagesize = int(self.get_argument("pagesize"))
        if not await self.question_allow:
            raise PermissionDeniedError("没有访问权限")
        list = await self.db.answer.get_answers(question_id,page,pagesize)
        for answer in list:
            answer_id = answer['_id']
            answer['upvote_count'] = await self.db.vote.get_up_vote_count(answer_id)
            answer['downvote_count'] = await self.db.vote.get_down_vote_count(answer_id)
            answer['is_upvoted'] = await self.db.vote.is_up_voted(answer_id, await self.user_id)
            answer['is_downvoted'] = await self.db.vote.is_down_voted(answer_id, await self.user_id)
        self.finish_success(result=list)

class AnswerHandler(BaseHandler):

    """
        @api {get} /answer 获取单个回答
        @apiName GetAnswer
        @apiGroup Answer

        @apiParam {String} answer_id 答案id
        @apiParamExample {urlparams} Request-Example:
            {
                "answer_id": [回答id]
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": {
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
                'upvote_count': 0 # 支持者人数
                'downvote_count': 0 # 反对者人数
                'user_name':'' # 回答者用户名
                "upvote_list": [],
                "downvote_list": [
                    {
                        "_id": "5a0xxxxx",
                        "answer_id": "5a0xxxxx",
                        "user_id": "5a0xxxx",
                        "vote": false,
                        "user_name": "高睿昊"
                    }
                ]
            }
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def get(self):
        answer_id = self.get_argument("answer_id")
        if not await self.answer_allow:
            raise PermissionDeniedError("没有访问权限")
        answer = await self.db.answer.get_answer(answer_id)
        answer_id = answer['_id']
        answer['upvote_count'] = await self.db.vote.get_up_vote_count(answer_id)
        answer['downvote_count'] = await self.db.vote.get_down_vote_count(answer_id)
        answer['upvote_list'] = await self.db.vote.get_up_vote_list(answer_id)
        answer['downvote_list'] = await self.db.vote.get_down_vote_list(answer_id)
        answer['is_upvoted'] = await self.db.vote.is_up_voted(answer_id, await self.user_id)
        answer['is_downvoted'] = await self.db.vote.is_down_voted(answer_id, await self.user_id)
        self.finish_success(result=answer)


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


routes.handlers +=[
    (r'/answers',sAnswerHandler),
    (r'/answer',AnswerHandler)
]