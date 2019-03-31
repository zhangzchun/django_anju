from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from . import models
from company import models as com_models

# Create your views here.

# 设计师列表
def designerComList(request):
    if request.method == "GET":
        company_id = request.GET.get("company_id")
        if company_id :
            try:
                designer_info = com_models.companyInfo.objects.filter(id=company_id).values("designerinfo__id",
                                                                                            "designerinfo__name",
                                                                                            "designerinfo__case_num",
                                                                                            "designerinfo__icon")[0:4]
                res = list(designer_info)
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)



def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]



def designerListNum(request):
    if request.method == "GET":
        company_id = request.GET.get('company_id')
        if company_id:
            try:
                cursor = connection.cursor()
                cursor.execute("select count(c.id) as des_num\
                    from designer_designerinfo as d inner join company_companyinfo as c on d.company_id=c.id \
                    where company_id={company_id}".format(company_id=company_id))
                res = cursor.fetchone()
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


def designerPage(request):
    if request.method == "GET":
        company_id = request.GET.get('company_id')
        perPageNum = request.GET.get('perPageNum')
        pageNum = request.GET.get('pageNum') and int(request.GET.get('pageNum')) * int(perPageNum)

        if company_id:
            try:
                cursor = connection.cursor()
                cursor.execute("select  d.id ,d.icon as des_icon,d.`name` as des_name,d.case_num,d.design_concept\
                    from designer_designerinfo as d inner join company_companyinfo as c on d.company_id=c.id \
                    where company_id={company_id} limit {pageNum},{perPageNum}".format(company_id=company_id,pageNum=pageNum,perPageNum=perPageNum))
                res = dictfetchall(cursor)
                if res:
                    print(res)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

