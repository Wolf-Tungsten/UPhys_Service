from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError

class sQuestionHandler(BaseHandler):
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
    async def get(self):
        if not await self.question_allow:
            raise PermissionDeniedError("没有访问权限")
        question_id = self.get_argument("question_id")
        list = await self.db.question.get_question(question_id)
        answer_count = await self.db.answer.get_answer_count(question_id)
        list.update({"answer_count":answer_count})
        self.finish_success(result=list)

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
        await self.db.question.post_question(category_id,default_question,user_id)
        await self.db.user.change_exp(user_id,10)
        self.finish_success(result='ok')

    async def put(self):
        modify_user_id = await self.user_id
        question_id = self.get_argument("question_id")
        user_id = await self.db.question.get_user_id(question_id)
        if  not await self.is_admin and modify_user_id != user_id:
            raise PermissionDeniedError("没有修改权限")
        question = self.get_argument("question")
        await self.db.question.put_question(question_id,question,modify_user_id)
        self.finish_success(result='ok')


    async def delete(self):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        question_id = self.get_argument("question_id")
        user_id = self.db.question.get_user_id(question_id)
        await self.db.question.delete_question(question_id)
        await self.db.user.change_exp(user_id,-10)
        self.finish_success(result='ok')

routes.handlers +=[
    (r'/questions',sQuestionHandler),
    (r'/question',QuestionHandler)
]