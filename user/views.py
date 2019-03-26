from django.shortcuts import render
from django.http import JsonResponse
import json
from . import models
# Create your views here.




def unloadImg(request):
    if  request.method=="POST":
        img=json.loads(request.body)
        if img:
            img_info=models.userIcon.objects.create(**img)
            img_info.save
            if img_info:
                res=img_info.id
                return JsonResponse({"status_code": "10012", "status_text": "添加信息成功", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10013", "status_text": "添加信息失败"}, safe=False)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)