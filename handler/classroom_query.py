from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError, ResourceNotExistError


class ClassroomStudentHandler(BaseHandler):

    """
        @api {get} /classroom/student 获取问题题目
        @apiName Classroom-Get-Question
        @apiGroup Classroom

        @apiParam {String} code 问题code
        @apiParamExample {urlparams} Request-Example:
            {
                "code": [问题code]
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": {
                "user_id": '',  # 发布问题的老师的user_id
                "question": '',  # 问题的文本内容描述
                "image_url": '',  # 问题的附件图片
                "post_time": '',  # 问题的发布时间
                "code": ''  # 问题的code，用于学生找到问题
            }
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-ResourceNotExistError 没有访问权限

    """
    async def get(self, operator):
        if operator == '/question':
            code = self.get_argument("code")
            question = (await self.db.classroom_question.get_a_question_by_code(code))[0]
            question.pop('answer')
            # 删除问题的答案
            self.finish_success(result=question)
        elif operator == '/all_my_answers':
            page = self.get_argument("page")
            pagesize = self.get_argument("pagesize")
            student_id = await self.user_id
            result, count = await self.db.classroom_answer.get_answers_of_a_student(student_id, pagesize, page)
            self.finish_success(result={
                'answers': result,
                'count': count
            })
        else:
            raise ResourceNotExistError("操作不存在")



    """
        @api {post} /classroom/student 提交回答
        @apiName Classroom-Post-Answer
        @apiGroup Classroom

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
    async def post(self, operator):
        student_id = await self.user_id
        question_id = self.get_argument("question_id")
        answer = self.get_argument("answer")
        question = await self.db.classroom_question.get_a_question_by_id(question_id)
        await self.db.classroom_answer.answer_a_question(student_id, question_id, answer, question['answer'] == str(answer))
        self.finish_success(result="ok")


class ClassroomTeacherHandler(BaseHandler):
    async def get(self, operator):
        teacher_id = await self.user_id
        if operator == '/all_my_questions':
            pagesize = self.get_argument('pagesize')
            page = self.get_argument('page')
            result, count = await self.db.classroom_question.get_all_my_questions(teacher_id, pagesize, page)
            self.finish_success(result={
                'questions': result,
                'count': count
            })
        elif operator == '/answers':
            pagesize = self.get_argument('pagesize')
            page = self.get_argument('page')
            question_id = self.get_argument('question_id')
            result, count = await self.db.classroom_answer.get_answers_of_a_question(question_id=question_id,
                                                                                       pagesize=pagesize,
                                                                                       page=page)
            for answer in result:
                student_id = answer['student_id']
                user_info = await self.db.user.get_user_with_id(student_id)
                answer['student_name'] = user_info['name']
                answer['student_cardnum'] = user_info['cardnum']
            self.finish_success(result={
                'questions': result,
                'count': count
            })

    async def post(self, operator):
        user_id = await self.user_id
        if not (await self.is_admin):
            raise PermissionDeniedError('只允许管理员出题')
        question = self.get_argument('question')
        image = self.get_argument('image')
        answer = self.get_argument('answer')
        code = await self.db.classroom_question.put_up_a_question(user_id, question, image, answer)
        self.finish_success(result={
            'code': code
        })

    async def delete(self, operator):
        if not await self.is_admin:
            raise PermissionDeniedError("需要管理员权限")
        question_id = self.get_argument('question_id')
        await self.db.classroom_question.delete_a_question(question_id)
        self.finish_success(result="ok")

routes.handlers += [
    (r'/classroom/student([A-Za-z_/]*)', ClassroomStudentHandler),
    (r'/classroom/teacher([A-Za-z_/]*)', ClassroomTeacherHandler)
]
