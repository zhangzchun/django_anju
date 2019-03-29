from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from . import models

# Create your views here.

# 公司列表页面
def companyList(request):
    if request.method=="GET":
        try:
            company_list=models.companyInfo.objects.all().values("id","name","contact_tel","case_num","work_site_num","company_icon","companyimg__name")
            res=list(company_list)
            if res:
                return JsonResponse({"status_code": "10009", "status_text":"找到数据","content": res},safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


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


# 公司详情
def companyDetail(request):
    if request.method == "GET":
        company_id=request.GET.get("company_id")
        if company_id:
            try:
                company_info=models.companyInfo.objects.filter(id=company_id).values("companyimg__name","name","mouth_value","bond","contact_tel","case_num","work_site_num","favorable_rate","address")
                res=list(company_info)
                if res:
                    return JsonResponse({"status_code": "10009", "status_text":"找到数据","content": res},safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code":"40006","status_text":"请求方式错误"}, safe=False)


# 公司列表排序
def companySort(request):
    if request.method=="GET":
        detail=request.GET.get("detail")
        if detail:
            if detail=="综合":
                sort_condition="id"
            elif detail=="案例":
                sort_condition = "-case_num"
            elif detail=="工地":
                sort_condition = "-work_site_num"
            elif detail=="信用":
                sort_condition = "-favorable_rate"

            try:
                company_list = models.companyInfo.objects.all().values("id", "name", "contact_tel", "case_num",
                             "work_site_num", "company_icon", "companyimg__name").order_by(sort_condition)
                res = list(company_list)
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


#公司列表筛选
def companyScreen(request):
    pass
