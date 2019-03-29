# 加密模块
import jwt
# 装饰器
from functools import wraps
# json
import json

SECRECT_KEY='123456'


# 构建token
def createToken(user_id):
    import datetime
    import hashlib
    # 当前时间加上180秒，意味着token过期时间为3分钟以后
    datetimeInt = datetime.datetime.utcnow() + datetime.timedelta(seconds=60*6)
    option = {
        'iss': 'jobapp.com',  # token的签发者
        'exp': datetimeInt,  # 过期时间
        'iat': datetime.datetime.utcnow(),
        'aud': 'webkit',  # token的接收者，这里指定为浏览器
        'user_id': user_id  # 放入用户信息，唯一标识，解析后可以使用该消息
    }
    # encoded2 = jwt.encode(payload=option,key= SECRECT_KEY, algorithm='HS256',options= {'verify_exp':True})
    # 这时token类型为字节类型，如果传个前端要进行token.decode()
    token = jwt.encode(option, SECRECT_KEY, 'HS256')
    # print(token)
    return token.decode()


# 验证token
def checkToken(token):
    try:
        decoded = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        return decoded['user_id']
    except jwt.ExpiredSignatureError as ex:
        return None


# 检查登录状态
def checkLogin(request):
    def decorated(func):
        @wraps(func)
        def wrapper():
            try:
                token=request.headers.get('token')
                decoded = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
                return func()
            except jwt.ExpiredSignatureError as ex:
                return json.dumps({"status_code":"10006","status_text":"登录过期"})
        return wrapper
    return decorated


