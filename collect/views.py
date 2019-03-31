from django.shortcuts import render
from django.http import JsonResponse
import json
from . import models
from company import models as com_models
from django.db import connection, connections


# Create your views here.

# 增加收藏
def increaseCollection(request):
    if request.method == "POST":
        collect = json.loads(request.body)
        print(collect)
        if collect:
            collect_info = models.collectInfo.objects.create(**collect)
            collect_info.save()
            collect_id = collect_info.id
            if collect_id:
                res = {"collect_id": collect_id}
                return JsonResponse({"status_code": "10030", "status_text": "收藏成功", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10031", "status_text": "收藏失败"}, safe=False)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 取消收藏
def cancelCollection(request):
    if request.method == "POST":
        collect_id = json.loads(request.body)
        if collect_id:
            affect_rows = models.collectInfo.objects.filter(id=collect_id['collect_id']).delete()
            if affect_rows:
                return JsonResponse({"status_code": "10040", "status_text": "取消收藏成功"}, safe=False)
            else:
                return JsonResponse({"status_code": "10041", "status_text": "取消收藏失败"}, safe=False)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 检查是否收藏
def checkCollection(request):
    if request.method == "POST":
        collect = json.loads(request.body)
        if collect:
            collect_id = models.collectInfo.objects.filter(content_id=collect['content_id'],
                                                           collectType_id=collect['collectType_id'],
                                                           user_id=collect['user_id']).values("id")
            if collect_id:
                res = list(collect_id)
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取收藏日记
def diaryCollections(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                cursor = connection.cursor()
                sql = "SELECT c.id, d.id diary_id ,u.nickname,ui.icon , d.diary_title , s.`name` style_name ,d.company\
                 ,c.collect_date ,dc.diary_content,(SELECT group_concat(di.diary_img) FROM diary_diaryimg di WHERE\
                  di.diaryContent_id = dc.id && dc.diary_id=d.id) diary_img FROM collect_collectinfo c INNER JOIN\
                   user_userinfo u INNER JOIN user_usericon ui INNER JOIN diary_diaryinfo d INNER JOIN \
                   search_style s INNER JOIN diary_diarycontent dc on  u.id=ui.user_id and c.content_id=d.id and\
                  d.user_id=u.id and d.style_id=s.id  and d.id=dc.diary_id where c.user_id={user_id}  and c.collectType_id=1 \
                  and dc.stage='前期准备' ".format(user_id=user_id)
                cursor.execute(sql)
                res = dictfetchall(cursor)
                if res:
                    for i in range(len(res)):
                        diary_img = res[i]["diary_img"].split(",")
                        res[i]["diary_img"] = diary_img
                    for r in res:
                        r["check"] = False
                        r["checkNum"] = 1
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取收藏的攻略
def strategyCollections(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                cursor = connection.cursor()
                sql = "select c.id, s.id , si.strategy_img,s.strategy_title, sc.lead, c.collect_date \
                        from collect_collectinfo c INNER JOIN collect_collecttype ct INNER JOIN user_userinfo u \
                        INNER JOIN strategy_strategyinfo s INNER JOIN strategy_strategycontent sc INNER JOIN strategy_strategyimg si\
                        on c.collectType_id = ct.id and c.user_id =u.id and c.content_id=s.id and s.id=sc.strategy_id \
                        and si.strategy_id=s.id where c.user_id={user_id} and c.collectType_id=2 ".format(user_id=user_id)
                cursor.execute(sql)
                res = dictfetchall(cursor)
                if res:
                    for r in res:
                        r["check"] = False
                        r["checkNum"] = 1
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取收藏的公司
def companyCollections(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                res=list(models.collectInfo.objects.filter(user_id=user_id,collectType_id=3).values("id","content_id","collect_date"))
                if res:
                    for r in res:
                        com_info=list(com_models.companyInfo.objects.filter(id=r["content_id"]).values("company_icon","name","case_num","work_site_num","contact_tel"))
                        r.update(com_info[0])
                        r["check"] = False
                        r["checkNum"] = 1
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 获取收藏的案例
def caseCollections(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                cursor = connection.cursor()
                sql = "select c.id, case_caseinfo.id ,ci.img_url,case_caseinfo.`name`, case_caseinfo.area, s.`name` style_name, \
                        ht.`name` houseType, rt.`name` renovation_type, case_caseinfo.cost, c.collect_date \
                        from collect_collectinfo c INNER JOIN case_caseinfo INNER JOIN case_caseimg ci \
                        INNER JOIN search_style s INNER JOIN user_housetype ht INNER JOIN search_renovationtype rt\
                        on c.content_id=case_caseinfo.id and case_caseinfo.id=ci.case_id and case_caseinfo.style_id=s.id \
                        and case_caseinfo.houseType_id=ht.id and case_caseinfo.renovationType_id=rt.id\
                        where c.user_id={user_id} and c.collectType_id=4 GROUP BY case_caseinfo.id ".format(user_id=user_id)
                cursor.execute(sql)
                res = dictfetchall(cursor)
                if res:
                    for r in res:
                        r["check"] = False
                        r["checkNum"] = 1
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 返回字典对象
def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
