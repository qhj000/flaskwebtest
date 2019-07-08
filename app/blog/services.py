from functools import wraps

from app import app
from flask import request
import jwt
import datetime
from werkzeug.exceptions import abort
from app.blog.models import User

AUTH_EXPIRE = 8 * 60 * 60  # 8小时过期


# 生成token
def gen_token(user_id):
    """生成token"""
    return jwt.encode({  # 增加时间戳，判断是否重发token或重新登录
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE  # 要取整
    }, app.config['SECRET_KEY'], 'HS256').decode()  # decode，bytes变字符串


# print(gen_token('hello'))

# 采用装饰器认证token,
def authenticate(controller):
    @wraps(controller)  # 装饰器的修复
    def wrapper():
        # 自定义header jwt
        payload = request.headers['JWT']

        if not payload:  # None没有拿到，认证失败
            return abort(401)
        # print(payload)
        try:  # 解码，同时验证过期时间
            payload = jwt.decode(payload, app.config['SECRET_KEY'], algorithms=['HS256'])
            # print(payload)
        except:
            return abort(401)

        try:
            user_id = payload.get('user_id', -1)
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise
            request.user = user  # 如果正确，则注入user
            print(request.user)
            print('-' * 30)
        except Exception as e:
            print(e)
            return abort(401)

        # ret = controller()  # 调用视图函数
        return controller()

    return wrapper
