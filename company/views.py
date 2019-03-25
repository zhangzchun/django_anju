from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from . import models

# Create your views here.

# 公司列表页面
def companyList(request):
    pass

# 首页公司列表
def indexCompanyList(request):
    if request.method == "GET":
        try:
            index_company=models.companyInfo.objects.all().values("name","id","companyimg__name","company_icon")[0:8]
            res=list(index_company)
            if res:
                return JsonResponse({"status_code": "10009", "status_text":"找到数据","content": res},safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code":"40006","status_text":"请求方式错误"}, safe=False)


