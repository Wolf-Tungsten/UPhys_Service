from handler.base import BaseHandler
import routes
from handler.exceptions import PermissionDeniedError, ResourceNotExistError


class VoteHandler(BaseHandler):

    async def get(self, *args, **kwargs):
        raise ResourceNotExistError("POST/DELETE ONLY")
    """
        @api {post} /vote 支持一个回答
        @apiName UpVote
        @apiGroup Vote

        @apiParam {String} answer_id 回答id

        @apiParamExample {json} Request-Example:
            {
                "answer_id": [回答id],
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": [true # 支持成功|false # 盲目支持]
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def post(self):
        user_id = await self.user_id
        answer_id = self.get_argument("answer_id")
        if not await self.answer_allow:
            raise PermissionDeniedError("没有访问权限")
        result = await self.db.vote.up_vote(answer_id, user_id)
        self.finish_success(result=result)


    """
        @api {delete} /vote 踩一个回答
        @apiName DownVote
        @apiGroup Vote

        @apiParam {String} answer_id 回答id

        @apiParamExample {json} Request-Example:
            {
                "answer_id": [回答id],
            }
        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": "success",
            "code": "200",
            "result": [true #  踩成功|false # 盲目踩]
        }

        @apiError 401-AuthError 身份认证失败
        @apiError 404-PermissionDeniedError 没有访问权限

    """
    async def delete(self):
        user_id = await self.user_id
        answer_id = self.get_argument("answer_id")
        if not await self.answer_allow:
            raise PermissionDeniedError("没有访问权限")
        result = await self.db.vote.down_vote(answer_id, user_id)
        self.finish_success(result=result)

routes.handlers += [
    (r'/vote', VoteHandler),
]