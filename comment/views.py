from django.shortcuts import render
from . import models
from django.http import HttpResponse, response, JsonResponse
from django.db.models import F
import json
from django.db import connection, connections


# Create your views here.

# 获取评论
def getComments(request):
    if request.method == "GET":
        id = request.GET
        try:
            for i in id.keys():
                if i == "strategy_id":
                    commentType_id = 1
                elif i == "diary_id":
                    commentType_id = 2
                comment_info = models.commentInfo.objects.filter(comment_obj_id=id[i],
                                                                 commentType_id=commentType_id).values(
                    "id", "fromu_id", "fromu__userIcon__icon", "fromu__nickname", "comment_content", "comment_time",
                    "comment_num").order_by("-comment_time","-comment_num")
                res = list(comment_info)
            if res:
                for i in range(len(res)):
                    comment_time = str(res[i]["comment_time"]).replace("-", "/").split("+")[0]
                    res[i]["comment_time"] = comment_time
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取回复
def getReplys(request):
    if request.method == "GET":
        comment_id = request.GET.get("comment_id")
        try:
            reply_info = models.replyInfo.objects.filter(comment_id=comment_id).values(
                "id", "fromu_id", "comment_id", "fromu__userIcon__icon", "fromu__nickname", "reply_content",
                "reply_time", "tou_nickname").order_by("-reply_time")
            res = list(reply_info)
            if res:
                for i in range(len(res)):
                    reply_time = str(res[i]["reply_time"]).replace("-", "/").split("+")[0]
                    res[i]["reply_time"] = reply_time
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 插入评论
def addComment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            comment = models.commentInfo.objects.create(**data)
            comment.save()
            if comment.id:
                comment_info = models.commentInfo.objects.filter(comment_obj_id=data["comment_obj_id"],
                                                                 commentType_id=data["commentType_id"]).values(
                    "id", "fromu_id", "fromu__userIcon__icon", "fromu__nickname", "comment_content", "comment_time",
                    "comment_num").order_by("-comment_time","-comment_num")
                res = list(comment_info)
                if res:
                    for i in range(len(res)):
                        comment_time = str(res[i]["comment_time"]).replace("-", "/").split("+")[0]
                        res[i]["comment_time"] = comment_time
                    return JsonResponse({"status_code": "10010", "status_text": "评论成功", "content": res}, safe=False)
            return JsonResponse({"status_code": "10011", "status_text": "评论失败"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 插入回复
def addReply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        try:
            reply = models.replyInfo.objects.create(**data)
            reply.save()
            if reply.id:
                affect_rows = models.commentInfo.objects.filter(id=data["comment_id"]).update(comment_num = F("comment_num") + 1)
                comment_num=list(models.commentInfo.objects.filter(id=data["comment_id"]).values("comment_num"))
                if affect_rows and comment_num:
                    reply_info = models.replyInfo.objects.filter(comment_id=data["comment_id"]).values(
                        "id", "fromu_id", "comment_id", "fromu__userIcon__icon", "fromu__nickname", "reply_content",
                        "reply_time", "tou_nickname").order_by("-reply_time")
                    res = list(reply_info)
                    if res:
                        for i in range(len(res)):
                            reply_time = str(res[i]["reply_time"]).replace("-", "/").split("+")[0]
                            res[i]["reply_time"] = reply_time
                        return JsonResponse({"status_code": "10010", "status_text": "评论成功","comment_num":comment_num ,"content": res}, safe=False)
            return JsonResponse({"status_code": "10011", "status_text": "评论失败"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


if __name__ == '__main__':
    data={'fromu_id': 1, 'comment_id': 74, 'reply_id': None, 'replyType_id': 1, 'reply_content': '测试一', 'tou_id': 1, 'tou_nickname': '瀚海百丈冰'}