from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError

class sAnswerHandler(BaseHandler):
    async def get(self):
        question_id = self.get_argument("question_id")
        page = self.get_argument("page")
        pagesize = self.get_argument("pagesize")
        if not await self.question_allow:
            raise PermissionDeniedError("没有访问权限")
        list = await self.db.answer.get_answers(question_id,page,pagesize)
        self.finish_success(result=list)

class AnswerHandler(BaseHandler):

    async def post(self):
        user_id =await self.user_id
        question_id = self.get_argument("question_id")
        if not await self.question_allow:
            raise PermissionDeniedError("没有访问权限")
        default_answer = self.db.answer.get_default()
        answer = self.get_argument("answer")
        for a in answer:
            default_answer[a] = answer[a]
        await self.db.answer.post_answer(question_id,default_answer,user_id)
        self.finish_success(result='ok')

    async def put(self):
        modify_user_id = await self.user_id
        answer_id = self.get_argument("answer_id")
        user_id = await self.db.answer.get_user_id(answer_id)
        if  not await self.is_admin and modify_user_id != user_id:
            raise PermissionDeniedError("没有修改权限")
        answer = self.get_argument("answer")
        await self.db.answer.put_answer(answer_id,answer,modify_user_id)
        self.finish_success(result='ok')


    async def delete(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        answer_id = self.get_argument("answer_id")
        await self.db.answer.delete_answer(answer_id)
        self.finish_success(result='ok')

class VoteHandler(BaseHandler):
    async def post(self):
        user_id = await self.user_id
        answer_id = self.get_argument("answer_id")
        if not await self.answer_allow:
            raise PermissionDeniedError("没有访问权限")
        await self.db.answer.post_answer_vote(answer_id,user_id)
        self.finish_success(result='ok')

    async def delete(self):
        user_id = await self.user_id
        answer_id = self.get_argument("answer_id")
        if not await self.answer_allow:
            raise PermissionDeniedError("没有访问权限")
        await self.db.answer.delete_answer_vote(answer_id,user_id)
        self.finish_success(result='ok')

routes.handlers +=[
    (r'/answers',sAnswerHandler),
    (r'/answer',AnswerHandler),
    (r'/answer/vote',VoteHandler)
]