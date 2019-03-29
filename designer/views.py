from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from . import models
from company import models as com_models

# Create your views here.

# 设计师列表
def designerList(request):
    if request.method == "GET":
        company_id = request.GET.get("company_id")
        type = request.GET.get("type")
        if company_id and type:
            try:
                if type == "designerList":
                    designer_info = com_models.companyInfo.objects.filter(id=company_id).values("designerinfo__id",
                                                                                                "designerinfo__name",
                                                                                                "designerinfo__case_num",
                                                                                                "designerinfo__icon",
                                                                                                "designerinfo__design_concept")
                elif type == "companyDesignerList":
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
