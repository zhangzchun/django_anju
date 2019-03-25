from django.shortcuts import render
from . import models
from django.http import HttpResponse, response, JsonResponse
from django.db import connection, connections


# Create your views here.

# 攻略列表
def strategyList(request):
    if request.method == "GET":
        try:
            strategy_content = models.strategyInfo.objects.all().values("id", "strategy_title", "author",
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


# 攻略详情
def strategyDetail(request):
    if request.method == "GET":
        strategy_id = request.GET.get("strategy_id")
        try:
            strategy_content = models.strategyInfo.objects.filter(id=strategy_id).values("id", "strategy_title",
                                                                                         "author", "publish_date",
                                                                                         "strategycontent__lead",
                                                                                         "strategycontent__strategy_content")
            # strategy_content = [{'id': _.id, 'strategy_title':_.strategy_title,'author':_.author, 'nick': _.coreuserwxprofile__nickname} for _ in strategy_content]
            res = list(strategy_content)
            if res:
                publish_date = str(res[0]["publish_date"]).replace("-", "/").split("+")[0]
                res[0]["publish_date"] = publish_date
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 首页攻略标题
def strategyTitle(request):
    if request.method == "GET":
        try:
            strategy_content = models.strategyInfo.objects.all().values("id", "strategy_title").order_by("id")[0:6]
            res = list(strategy_content)
            if res:
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)
