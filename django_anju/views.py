from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import uuid
import json

# Create your views here.
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
