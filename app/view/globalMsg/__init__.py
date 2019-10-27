from flask import Blueprint, request, jsonify, make_response
from flask.globals import LocalProxy, partial, _request_ctx_stack, _lookup_req_object
from app.utils.socketioUtils import SocketRedis
from app.model.constant import msg_map, MsgHandler
from functools import wraps
import json


gb = Blueprint('globals', __name__)


# @gb.before_app_request
# def authorization():
#     user_token = request.headers.get('tk')
#     if not user_token:
#
#     else:
#         userInfo=Token.unpackTk(current_app.config,user_token)
#         if not userInfo:
#             print('userinfo,',userInfo)
#             response=make_response(json.dumps({'code':RET.TOKENERR,'msg':error_map[RET.TOKENERR],'data':'1'},ensure_ascii=False))
#             response.delete_cookie('tk')
#             return response
#         t=User.query.filter(User.userName==userInfo['userName']).first()
#         t.user=t
#         t.pre='user'
#     ctx = _request_ctx_stack()
#     ctx.token = t


#socket权限验证
def SocketAuth(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        t = SocketRedis.get()
        if not t:
            return {'code': MsgHandler.UserTokenError, 'msg': msg_map[MsgHandler.UserTokenError], 'data': '1'}
        ctx = _request_ctx_stack()
        ctx.token = json.loads(t)
        return func(self, *args, **kwargs)
    return wrap


token = LocalProxy(partial(_lookup_req_object, 'token'))