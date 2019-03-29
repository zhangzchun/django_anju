from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import uuid
from user import models as umodels
import urllib
import random
import http

# Create your views here.
# 七牛token接口
def qiniuToken(request):
    from qiniu import Auth, put_file,etag
    if request.method == "GET":
        try:
            # 填写七牛云的Access Key 和 Secret Key
            access_key = 'cawrGaqKSnrK7ATg34BRwhzfoMrGMeudW6kXsEU_'
            secret_key = '7HzCpLWvfWZp1kHgqOruxd-WXvMsZGW5YlTWS7U8'
            # 构建鉴权对象
            q=Auth(access_key,secret_key)
            # 要上传的空间
            bucket_name = 'anju_image'
            filename=request.GET.get('filename')
            print(filename)
            # 上传到七牛云后保存的文件名
            key = str(uuid.uuid4())+'.'+filename.split('.')[1]
            # 生成上传token，可以指定过期时间等
            token=q.upload_token(bucket_name,key,3600)
            domain = 'http://porcbrvf3.bkt.clouddn.com'

            return  JsonResponse({"code": "908", "qiniu_token": token,'key':key,'domain':domain})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})



# 短信验证接口

# 请求的路径
host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"
# 用户名是登录ihuyi.com账号名（例如：cf_demo123）
account = "C94040688"
# 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
password = "f1fb3fa1e49321ed34023b0a63d40300    "

def sendMessage(request):
    """发送信息的视图函数"""
    # 获取ajax的get方法发送过来的手机号码
    telephone = request.GET.get('telephone')
    # 通过手机去查找用户是否已经注册
    user = umodels.userInfo.objects.filter(telephone=telephone)
    if len(user) == 1:
        return JsonResponse({'msg': "该手机已经注册"})
    # 定义一个字符串,存储生成的6位数验证码
    message_code = ''
    for i in range(6):
        i = random.randint(0, 9)
        message_code += str(i)
    # 拼接成发出的短信
    text = "您的验证码是：" + message_code + "。请不要把验证码泄露给其他人。"
    # 把请求参数编码
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': telephone, 'format': 'json'})
    # 请求头
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # 通过全局的host去连接服务器
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    # 向连接后的服务器发送post请求,路径sms_send_uri是全局变量,参数,请求头
    conn.request("POST", sms_send_uri, params, headers)
    # 得到服务器的响应
    response = conn.getresponse()
    # 获取响应的数据
    response_str = response.read()
    # 关闭连接
    conn.close()
    # 把验证码放进session中
    request.session['message_code'] = message_code
    print(eval(response_str.decode()))
    # 使用eval把字符串转为json数据返回
    return JsonResponse(eval(response_str.decode()))
