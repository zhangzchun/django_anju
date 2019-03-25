from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from django.db import connection, connections
from company import models
from strategy import models as strategyModels

# Create your views here.

# 搜索公司
def searchCompany(request):
    pass

# 搜索攻略
def searchStrategy(request):
    if request.method == "GET":
        search_content = request.GET.get("search_content")
        try:
            strategy_content = strategyModels.strategyInfo.objects.filter(strategy_title__contains=search_content).values("id", "strategy_title", "author",
                                                                        "strategycontent__lead",
                                                                        "strategyimg__strategy_img").order_by("id")
            res = list(strategy_content)
            if res:
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 搜索日记
def searchDiary(request):
    if request.method == "GET":
        search_content=request.GET.get("search_content")
        try:
            cursor = connection.cursor()
            sql = "SELECT d.id diary_id ,u.nickname , ui.icon , d.diary_title , s.`name` style_name ,d.company , d.publish_date,\
                    dc.diary_content,(SELECT group_concat(di.diary_img) FROM diary_diaryimg di  \
                    WHERE di.diaryContent_id = dc.id && dc.diary_id=d.id) diary_img \
                    FROM user_userinfo u INNER JOIN user_usericon ui INNER JOIN diary_diaryinfo d INNER JOIN search_style s \
                    INNER JOIN search_renovationtype rt INNER JOIN diary_diarycontent dc \
                    on u.userIcon_id=ui.id  && d.user_id=u.id && d.style_id=s.id && d.renovationType_id=rt.id && d.id=dc.diary_id \
                    where dc.stage='前期准备' and d.diary_title like '%{search_content}%' order by d.publish_date desc".format(search_content=search_content)

            cursor.execute(sql)
            res = dictfetchall(cursor)
            if res:
                for i in range(len(res)):
                    diary_img = res[i]["diary_img"].split(",")
                    res[i]["diary_img"] = diary_img
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
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
