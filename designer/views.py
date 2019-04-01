from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from . import models
from company import models as com_models
from django.db import connection, connections
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



def designerDetailListNum(request):
    if request.method == "GET":
        designer_id = request.GET.get('designer_id')
        if designer_id:
            try:
                cursor = connection.cursor()
                cursor.execute("select  count(DISTINCT caseinfo.id) as caseNum\
                                from case_caseinfo as caseinfo INNER JOIN case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and\
                                designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where  designer.id={designer_id}".format(designer_id=designer_id))
                res = cursor.fetchone()
                if res:
                    print(res[0])
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)



def designerDetailList(request):
    if request.method == "GET":
        designer_id = request.GET.get('designer_id')
        perPageNum = request.GET.get('perPageNum')
        pageNum = request.GET.get('pageNum') and int(request.GET.get('pageNum')) * int(perPageNum)
        if designer_id:
            try:
                cursor = connection.cursor()
                cursor.execute("select  caseinfo.id,caseinfo.name as case_name,ht.name as house_type,rt.name as reno_type,ci.img_url as case_src,caseinfo.area,caseinfo.cost,style.`name` as  house_style \
                                from case_caseinfo as caseinfo inner join case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where  designer.id={designer_id} \
                                GROUP BY caseinfo.id LIMIT {pageNum},{perPageNum}".format(designer_id=designer_id,pageNum=pageNum,perPageNum=perPageNum))
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


def getDesignerInfo(request):
    if request.method == "GET":
        designer_id = request.GET.get('designer_id')

        if designer_id:
            try:
                cursor = connection.cursor()
                cursor.execute("select  d.id ,d.icon as des_icon,d.`name` as des_name,d.case_num,d.design_concept,d.personal_profile\
                    from designer_designerinfo as d inner join company_companyinfo as c on d.company_id=c.id \
                    where d.id={designer_id}".format(designer_id=designer_id))
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