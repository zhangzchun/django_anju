from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
import json
from . import models
from company import models as com_models

from django.db import connection, connections

# from django.core import serializers
# from django.db.models import Q, Count, Max, Min, Sum, Avg


# Create your views here.

# "将游标返回的结果保存到一个字典对象中"
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# 获取案例的数量,用于分页
def getCaseNum(request):
    if request.method == "GET":
        company_id = request.GET.get('company_id')
        if company_id:
            try:
                res = com_models.companyInfo.objects.filter(id=company_id).values(
                    "designerinfo__caseinfo__name").count()
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


# 获取符合条件的案例数量,用于筛选分页
def getConditionCaseNum(request):
    if request.method == "GET":
        condition=request.GET.get('CA')
        con=judgeCondition(condition)
        print(con)
        HT = request.GET.get('HT')
        CS = request.GET.get('CS')
        CA = request.GET.get('CA')
        company_id = request.GET.get('company_id')
        area_min = con.get('area_min')
        area_max = con.get('area_max')

        if HT and CS and CA:
            try:
                cursor = connection.cursor()
                cursor.execute("select  count(caseinfo.id) \
                                from case_caseinfo as caseinfo   INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on  caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where ht.name='{house_type}' and style.`name`='{case_style}' and '{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}' and  designer.company_id={company_id}\
                                ".format(house_type=HT,case_style=CS,area_min=area_min,area_max=area_max,company_id=company_id))

                res = cursor.fetchone()
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif (HT == "" and CS == "" and area_max != "") or \
             (HT == "" and CS != "" and area_max == "") or \
             (HT != "" and CS == "" and area_max == "") :
            try:
                cursor = connection.cursor()
                cursor.execute("select  count(caseinfo.id)\
                                from case_caseinfo as caseinfo  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on  caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where ht.`name`='{ht}' or style.`name`='{cs}' or ('{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}') and  designer.company_id={company_id}\
                                ".format(ht=HT,cs=CS,area_min=area_min,area_max=area_max,company_id=company_id))
                res = cursor.fetchone()
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif HT=="" and CS=="" and CA=="":
            try:
                cursor = connection.cursor()
                cursor.execute("select  count(caseinfo.id) \
                                from case_caseinfo as caseinfo  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on  caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where designer.company_id={company_id}\
                                ".format(company_id=company_id))
                res = cursor.fetchone()
                if res:

                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            try:
                cursor = connection.cursor()
                cursor.execute("select  count(caseinfo.id) \
                                from case_caseinfo as caseinfo  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on  caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where ((ht.`name`= '{ht}' and style.`name`='{cs}') or (ht.`name`='{ht}' and '{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}') \
                                or (style.`name`='{cs}' and '{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}'))and designer.company_id={company_id} \
                                ".format(ht=HT,cs=CS,area_min=area_min,area_max=area_max,company_id=company_id))
                res = cursor.fetchone()
                if res:
                    print(res)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取第一页的案例
def getCase(request):
    if request.method == "GET":
        company_id = request.GET.get('company_id')
        if company_id:
            try:
                cursor = connection.cursor()
                cursor.execute("select  caseinfo.id,caseinfo.name as case_name,ht.name as house_type,rt.name as reno_type,ci.img_url as case_src,caseinfo.area,caseinfo.cost,style.`name` as  house_style \
                                from case_caseinfo as caseinfo inner join case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where  designer.company_id={company_id}\
                                GROUP BY caseinfo.id LIMIT 0,20".format(company_id=company_id))
                res = dictfetchall(cursor)

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

# 获取前六条案例,放置在公司详情页
def getCompanyCase(request):
    if request.method == "GET":
        company_id = request.GET.get('company_id')
        if company_id:
            try:
                cursor = connection.cursor()
                cursor.execute("select  caseinfo.id,caseinfo.name as case_name,ht.name as house_type,rt.name as reno_type,ci.img_url as case_src,caseinfo.area,caseinfo.cost,style.`name` as  house_style \
                                from case_caseinfo as caseinfo inner join case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where  designer.company_id={company_id}\
                                GROUP BY caseinfo.id LIMIT 0,6".format(company_id=company_id))
                res = dictfetchall(cursor)

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


# 将面积取出最大值和最小值
def judgeCondition(condition):
    con={}
    if condition:
        if condition=="60m²以下":
            con.setdefault('area_min', '0')
            con.setdefault('area_max', '60')
        elif condition=="60-80m²":
            con.setdefault('area_min', '60')
            con.setdefault('area_max', '80')
        elif condition=="80-100m²":
            con.setdefault('area_min', '80')
            con.setdefault('area_max', '100')
        elif condition=="100-120m²":
            con.setdefault('area_min', '100')
            con.setdefault('area_max', '120')
        elif condition=="120-150m²":
            con.setdefault('area_min', '120')
            con.setdefault('area_max', '150')
        elif condition=="150-180m²":
            con.setdefault('area_min', '150')
            con.setdefault('area_max', '180')
        elif condition == "180-200m²":
            con.setdefault('area_min', '180')
            con.setdefault('area_max', '200')
        elif condition == "200-250m²":
            con.setdefault('area_min', '200')
            con.setdefault('area_max', '250')
        elif condition == "250m²以上":
            con.setdefault('area_min', '250')
            con.setdefault('area_max', '999')
    else:
        con.setdefault('area_min', '')
        con.setdefault('area_max', '')

    return con


# 获取符合条件的案例
def getConditionCase(request):
    if request.method == "GET":
        condition=request.GET.get('CA')
        con=judgeCondition(condition)
        HT = request.GET.get('HT')
        CS = request.GET.get('CS')
        CA = request.GET.get('CA')
        perPageNum=request.GET.get('perPageNum')
        pageNum = request.GET.get('pageNum') and int(request.GET.get('pageNum')) * int(perPageNum)
        company_id = request.GET.get('company_id')
        area_min = con.get('area_min')
        area_max = con.get('area_max')


        if HT and CS and CA:
            try:
                cursor = connection.cursor()
                cursor.execute("select  caseinfo.id,caseinfo.name as case_name,ht.name as house_type,rt.name as reno_type,ci.img_url as case_src,caseinfo.area,caseinfo.cost,style.`name` as  house_style \
                                from case_caseinfo as caseinfo inner join case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where ht.name='{house_type}' and style.`name`='{case_style}' and '{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}' and  designer.company_id={company_id}\
                                GROUP BY caseinfo.id LIMIT {pageNum},{perPageNum}".format(house_type=HT,case_style=CS,area_min=area_min,area_max=area_max,company_id=company_id,pageNum=pageNum,perPageNum=perPageNum))

                res = dictfetchall(cursor)

                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif (HT == "" and CS == "" and area_max != "") or \
             (HT == "" and CS != "" and area_max == "") or \
             (HT != "" and CS == "" and area_max == "") :
            try:
                cursor = connection.cursor()
                cursor.execute("select  caseinfo.id,caseinfo.name as case_name,ht.name as house_type,rt.name as reno_type,ci.img_url as case_src,caseinfo.area,caseinfo.cost,style.`name` as  house_style \
                                from case_caseinfo as caseinfo inner join case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where ht.`name`='{ht}' or style.`name`='{cs}' or ('{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}') and  designer.company_id={company_id}\
                                GROUP BY caseinfo.id LIMIT {pageNum},{perPageNum}".format(ht=HT,cs=CS,area_min=area_min,area_max=area_max,company_id=company_id,pageNum=pageNum,perPageNum=perPageNum))
                res = dictfetchall(cursor)
                if res:
                    print(res)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif HT=="" and CS=="" and CA=="":
            try:
                cursor = connection.cursor()
                cursor.execute("select  caseinfo.id,caseinfo.name as case_name,ht.name as house_type,rt.name as reno_type,ci.img_url as case_src,caseinfo.area,caseinfo.cost,style.`name` as  house_style \
                                from case_caseinfo as caseinfo inner join case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where designer.company_id={company_id}\
                                GROUP BY caseinfo.id LIMIT {pageNum},{perPageNum}".format(company_id=company_id,pageNum=pageNum,perPageNum=perPageNum))
                res = dictfetchall(cursor)
                if res:
                    print(res)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            try:
                cursor = connection.cursor()
                cursor.execute("select  caseinfo.id,caseinfo.name as case_name,ht.name as house_type,rt.name as reno_type,ci.img_url as case_src,caseinfo.area,caseinfo.cost,style.`name` as  house_style \
                                from case_caseinfo as caseinfo inner join case_caseimg as ci  INNER JOIN user_housetype as ht INNER JOIN search_renovationtype \
                                as rt INNER JOIN designer_designerinfo as designer INNER JOIN search_style as style \
                                on caseinfo.id=ci.case_id and caseinfo.houseType_id=ht.id and caseinfo.renovationType_id=rt.id and designer.id=caseinfo.designer_id and style.id=caseinfo.style_id\
                                where ((ht.`name`= '{ht}' and style.`name`='{cs}') or (ht.`name`='{ht}' and '{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}') \
                                or (style.`name`='{cs}' and '{area_min}'<=caseinfo.area  and caseinfo.area<='{area_max}'))and designer.company_id={company_id} \
                                GROUP BY caseinfo.id LIMIT {pageNum},{perPageNum}".format(ht=HT,cs=CS,area_min=area_min,area_max=area_max,company_id=company_id,pageNum=pageNum,perPageNum=perPageNum))
                res = dictfetchall(cursor)
                if res:
                    print(res)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)



# 获取案例详情

def getCaseDetail(request):
    if request.method == "GET":
        case_id=request.GET.get('case_id')
        try:
            cursor = connection.cursor()
            cursor.execute("select `case`.`name` as case_name,d.id as designer_id ,d.`name` as designer_name,d.icon as designer_icon,d.case_num,\
                            c.company_icon,ht.`name` as house_type,s.`name` as style,`case`.area,`case`.cost,rt.`name` as reno_type,\
                            `case`.duration, `case`.village as address\
                            from company_companyinfo as c INNER JOIN designer_designerinfo as d INNER JOIN case_caseinfo as `case` \
                            INNER JOIN search_style as s INNER JOIN user_housetype as ht INNER JOIN search_renovationtype as rt \
                            on  d.company_id=c.id and `case`.designer_id=d.id and  `case`.style_id=s.id\
                            and `case`.houseType_id=ht.id and `case`.renovationType_id=rt.id\
                            where `case`.id={case_id}".format(case_id=case_id))
            res = dictfetchall(cursor)
            if res:
                print(res)
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取案例详情图片
def getCaseDetailImg(request):
    if request.method == "GET":
        case_id=request.GET.get('case_id')
        try:
            cursor = connection.cursor()
            cursor.execute("select it.img_type as caseTypeSrc,ci.img_url as caseSrc,d.id as designer_id \
                            from case_caseimg as ci INNER JOIN case_imgtype as it INNER JOIN company_companyinfo as c INNER JOIN designer_designerinfo as d \
                            INNER JOIN case_caseinfo as `case` INNER JOIN search_style as s INNER JOIN user_housetype as ht INNER JOIN search_renovationtype as rt \
                            on ci.imgType_id=it.id and d.company_id=c.id and `case`.designer_id=d.id and ci.case_id=`case`.id and `case`.style_id=s.id\
                            and `case`.houseType_id=ht.id and `case`.renovationType_id=rt.id\
                            where `case`.id={case_id}".format(case_id=case_id))
            res = dictfetchall(cursor)
            if res:
                print(res)
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

"""

"""

