from django.shortcuts import render
from . import models
import json
from user import models as umodels
from django.http import HttpResponse, response, JsonResponse
from django.db import connection, connections


# Create your views here.

# 日记列表
def diaryList(request):
    if request.method == "GET":
        try:
            cursor = connection.cursor()
            sql = "SELECT d.id diary_id ,u.nickname , ui.icon , d.diary_title , s.`name` style_name ,d.company , d.publish_date,\
                    dc.diary_content,(SELECT group_concat(di.diary_img) FROM diary_diaryimg di  \
                    WHERE di.diaryContent_id = dc.id && dc.diary_id=d.id) diary_img \
                    FROM user_userinfo u INNER JOIN user_usericon ui INNER JOIN diary_diaryinfo d INNER JOIN search_style s \
                    INNER JOIN search_renovationtype rt INNER JOIN diary_diarycontent dc \
                    on u.id=ui.user_id  && d.user_id=u.id && d.style_id=s.id && d.renovationType_id=rt.id && d.id=dc.diary_id \
                    where dc.stage='前期准备' order by d.publish_date desc"

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


# 日记详情头部
def diaryDetailHeader(request):
    if request.method == "GET":
        diary_id = request.GET.get("diary_id")
        if diary_id:
            try:
                cursor = connection.cursor()
                sql = "SELECT d.id,u.nickname , ui.icon user_icon , d.diary_title ,d.publish_date,d.area, s.`name` style , \
                        rt.`name` type,d.village location ,d.company,d.browse_num,d.collect_num,d.comment_num\
                        FROM user_userinfo u INNER JOIN user_usericon ui INNER JOIN diary_diaryinfo d INNER JOIN search_style s INNER JOIN \
                        search_renovationtype rt on u.id=ui.user_id  && d.user_id=u.id && d.style_id=s.id && d.renovationType_id=rt.id\
                        where d.id={id}".format(id=diary_id)

                cursor.execute(sql)
                res = dictfetchall(cursor)
                if res:
                    publish_date = str(res[0]["publish_date"]).replace("-", "/").split("+")[0]
                    res[0]["publish_date"] = publish_date
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 日记详情内容
def diaryDetailContent(request):
    if request.method == "GET":
        diary_id = request.GET.get("diary_id")
        if diary_id:
            try:
                dairy_content = models.diaryContent.objects.filter(diary_id=diary_id).values("id", "stage",
                                                                                             "publish_date",
                                                                                             "diary_content")
                res01 = list(dairy_content)
                for r in res01:
                    diary_img = models.diaryImg.objects.filter(diaryContent_id=r.get("id")).values("diary_img")
                    res02 = list(diary_img)
                    r["diary_imgs"] = res02
                if res01:
                    print(res01)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res01}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 首页日记用户头像
def diaryUserIcon(request):
    if request.method == "GET":
        try:
            dairy_content = models.diaryInfo.objects.all().values("id","user_id").order_by("id")[0:12]
            res = list(dairy_content)
            if res:
                for r in res:
                    user_icon=list(umodels.userIcon.objects.filter(user_id=r["user_id"]).values("icon").order_by("-upload_date")[0:1])
                    r["user_icon"]=user_icon[0]["icon"]
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 首页日记展示
def indexDiary(request):
    if request.method == "GET":
        diary_id = request.GET.get("diary_id")
        if diary_id:
            try:
                cursor = connection.cursor()
                sql = "SELECT d.id diary_id , ui.icon , d.diary_title , s.`name` style_name ,d.company,\
                        dc.diary_content,(SELECT group_concat(di.diary_img) FROM diary_diaryimg di  \
                        WHERE di.diaryContent_id = dc.id && dc.diary_id=d.id) diary_img \
                        FROM user_userinfo u INNER JOIN user_usericon ui INNER JOIN diary_diaryinfo d INNER JOIN search_style s \
                        INNER JOIN search_renovationtype rt INNER JOIN diary_diarycontent dc \
                        on u.id=ui.user_id  && d.user_id=u.id && d.style_id=s.id && d.renovationType_id=rt.id && d.id=dc.diary_id \
                        where dc.stage='前期准备' and d.id={diary_id}".format(diary_id=diary_id)

                cursor.execute(sql)
                res = dictfetchall(cursor)
                if res:
                    diary_img = res[0]["diary_img"].split(",")
                    if len(diary_img) > 2:
                        diary_img = diary_img[0:2]
                    res[0]["diary_img"] = diary_img
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 首页日记标题
def diaryTitle(request):
    if request.method == "GET":
        try:
            diary_content = models.diaryInfo.objects.all().values("id", "diary_title").order_by("id")[0:6]
            res = list(diary_content)
            if res:
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取用户日记
def getUserDiary(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")

        if user_id:
            try:
                cursor = connection.cursor()
                sql = "select d.id,d.diary_title,d.publish_date,d.area,s.`name` as style, \
                        rt.`name` as reno_type,d.village,d.company,count(d.id) as count\
                        from diary_diaryinfo as d inner join search_style as s inner join search_renovationtype as rt \
                        inner join diary_diarycontent as dc on d.style_id = s.id \
                        and d.renovationType_id = rt.id and d.id = dc.diary_id \
                        where user_id = {id} group by d.id ".format(id=user_id)

                cursor.execute(sql)
                print('here')
                res = dictfetchall(cursor)

                for i in range(len(res)):
                    public_date = str(res[i]["publish_date"]).replace("-", "/")
                    res[i]["publish_date"] = public_date

                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)

            except Exception as ex:
                print('获取用户日记=>系统错误==>')
                print(ex)
                # 系统错误
                return JsonResponse({"status_code": "40004", "status_text": "系统错误"}, safe=False)
        else:
            # 信息错误
            # print("获取用户日记=>信息错误==>")
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)

    else:
        # 请求方式错误
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 添加用户日记
def addDiary(request):
    if request.method == "POST":
        body = request.body
        diary = body and json.loads(body)

        if diary:
            try:
                res = models.diaryInfo.objects.create(**diary)
                res.save()
                diary_id = res.id
                if diary_id:
                    return JsonResponse({"status_code": "10012", "status_text": "添加信息成功", "content": diary_id},
                                      safe=False)
                else:
                    return JsonResponse({"status_code": "10013", "status_text": "添加信息失败"}, safe=False)

            except Exception as ex:
                print('添加用户日记=>系统错误==>')
                print(ex)
                # 系统错误
                return JsonResponse({"status_code": "40004", "status_text": "系统错误"}, safe=False)
        else:
            # 信息错误
            # print("添加用户日记=>信息错误==>")
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)

    else:
        # 请求方式错误
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 编辑日记
def updaeDiary(request):
    if request.method == "POST":
        pass
    else:
        # 请求方式错误
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 写日记内容
def writeDiary(request):
    pass






# 返回字典对象
def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
