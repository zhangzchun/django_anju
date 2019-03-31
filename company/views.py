from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
from django.db import connection, connections
from . import models


# Create your views here.


# 首页公司列表
def indexCompanyList(request):
    if request.method == "GET":
        try:
            index_company = models.companyInfo.objects.all().values("name", "id", "companyimg__name", "company_icon")[
                            0:8]
            res = list(index_company)
            if res:
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            return ex
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 公司详情
def companyDetail(request):
    if request.method == "GET":
        company_id = request.GET.get("company_id")
        if company_id:
            try:
                company_info = models.companyInfo.objects.filter(id=company_id).values("companyimg__name", "name",
                                                                                       "mouth_value", "bond",
                                                                                       "contact_tel", "case_num",
                                                                                       "work_site_num",
                                                                                       "favorable_rate", "address")
                res = list(company_info)
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


# 公司列表排序
def companySort(request):
    if request.method == "GET":
        detail = request.GET.get("detail")
        if detail:
            if detail == "综合":
                sort_condition = "id"
            elif detail == "案例":
                sort_condition = "-case_num"
            elif detail == "工地":
                sort_condition = "-work_site_num"
            elif detail == "信用":
                sort_condition = "-favorable_rate"

            try:
                company_list = models.companyInfo.objects.all().values("id", "name", "contact_tel", "case_num",
                                                                       "work_site_num", "company_icon",
                                                                       "companyimg__name").order_by(sort_condition)
                res = list(company_list)
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# "将游标返回的结果保存到一个字典对象中"
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# 公司列表数量
def companyNum(request):
    if request.method == "GET":
        try:
            company = models.companyInfo.objects.all().count()
            if company:
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": company}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取符合条件的公司数量,用于筛选分页
def getConditionComNum(request):
    if request.method == "GET":
        price = request.GET.get('price')
        style = request.GET.get('style')
        address = request.GET.get('address')
        perPageNum = request.GET.get('perPageNum')
        pageNum = request.GET.get('pageNum') and int(request.GET.get('pageNum')) * int(perPageNum)

        if price and style and address:
            try:
                cursor = connection.cursor()
                cursor.execute("select count(DISTINCT c.id)\
                    from company_companyinfo as c  inner join search_price as price inner join \
                    search_style as style inner join company_companystyle as cs  \
                    on  c.price_id=price.id and style.id=cs.style_id and c.id=cs.company_id\
                    where price.`name`= '{price_name}' and style.`name`='{style_name}' and c.district='{district}' \
                    ".format(price_name=price, style_name=style, district=address))

                res = cursor.fetchone()
                print('1' * 10)
                print(res[0])
                if res:

                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif (price == "" and style == "" and address != "") or \
                (price == "" and style != "" and address == "") or \
                (price != "" and style == "" and address == ""):
            try:
                cursor = connection.cursor()

                cursor.execute(" select count(DISTINCT c.id)\
                    from company_companyinfo as c  inner join search_price as price inner join \
                    search_style as style inner join company_companystyle as cs  \
                    on  c.price_id=price.id and style.id=cs.style_id and c.id=cs.company_id\
                    where price.`name`= '{price_name}' or style.`name`='{style_name}' or c.district='{district}' \
                    ".format(price_name=price, style_name=style, district=address))
                res = cursor.fetchone()
                print('2' * 10)
                print(res[0])
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif price == "" and style == "" and address == "":
            try:
                res = models.companyInfo.objects.all().count()
                print('3' * 10)
                print(res)
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            try:
                cursor = connection.cursor()
                cursor.execute("select count(DISTINCT c.id) \
                    from company_companyinfo as c  inner join search_price as price inner join \
                    search_style as style inner join company_companystyle as cs  \
                    on  c.price_id=price.id and style.id=cs.style_id and c.id=cs.company_id\
                    where (price.`name`= '{price_name}' and style.`name`='{style_name}') or (price.`name`= '{price_name}' and c.district='{district}')\
                    or (style.`name`='{style_name}' and c.district='{district}') ORDER BY c.id".format(price_name=price,
                                                                                                       style_name=style,
                                                                                                       district=address))
                res = cursor.fetchone()
                print('4' * 10)
                print(res[0])
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res[0]}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 公司第一页页面
def companyList(request):
    if request.method == "GET":
        try:
            company = models.companyInfo.objects.all().values("id", "company_icon", "name", "case_num", "work_site_num",
                                                              "contact_tel", "companyimg__name")[0:5]
            res = list(company)
            if res:
                for r in res:
                    r["com_src"] = r.pop("companyimg__name")
                # print(res)
                return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取符合条件的公司
def getConditionCompany(request):
    if request.method == "GET":
        price = request.GET.get('price')
        style = request.GET.get('style')
        address = request.GET.get('address')
        perPageNum = int(request.GET.get('perPageNum'))
        pageNum = request.GET.get('pageNum') and int(request.GET.get('pageNum')) * int(perPageNum)
        pageNumber = request.GET.get('pageNum') and (int(request.GET.get('pageNum')) + 1) * int(perPageNum)

        if price and style and address:
            try:
                cursor = connection.cursor()
                cursor.execute("select distinct c.id,c.`name`,c.contact_tel,c.case_num,c.work_site_num,c.company_icon, ci.`name` as com_src\
                    from company_companyinfo as c inner join company_companyimg as ci inner join search_price as price inner join \
                    search_style as style inner join company_companystyle as cs  \
                    on c.id=ci.company_id and c.price_id=price.id and style.id=cs.style_id and c.id=cs.company_id\
                    where price.`name`= '{price_name}' and style.`name`='{style_name}' and c.district='{district}' \
                    ORDER BY c.id LIMIT {pageNum},{perPageNum}".format(price_name=price, style_name=style,
                                                                       district=address,
                                                                       pageNum=pageNum, perPageNum=perPageNum))

                res = dictfetchall(cursor)

                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif (price == "" and style == "" and address != "") or \
                (price == "" and style != "" and address == "") or \
                (price != "" and style == "" and address == ""):
            try:
                cursor = connection.cursor()

                cursor.execute(" select distinct c.id,c.`name`,c.contact_tel,c.case_num,c.work_site_num,c.company_icon, ci.`name`  as com_src\
                    from company_companyinfo as c inner join company_companyimg as ci inner join search_price as price inner join \
                    search_style as style inner join company_companystyle as cs  \
                    on c.id=ci.company_id and c.price_id=price.id and style.id=cs.style_id and c.id=cs.company_id\
                    where price.`name`= '{price_name}' or style.`name`='{style_name}' or c.district='{district}' \
                    group by c.id LIMIT {pageNum},{perPageNum}".format(price_name=price, style_name=style,
                                                                       district=address, pageNum=pageNum,
                                                                       perPageNum=perPageNum))
                res = dictfetchall(cursor)
                if res:
                    print(res)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        elif price == "" and style == "" and address == "":
            try:
                company = models.companyInfo.objects.all().values("id", "company_icon", "name", "case_num",
                                                                  "work_site_num", "contact_tel", "companyimg__name")[
                          pageNum:pageNumber]
                res = list(company)
                if res:
                    for r in res:
                        r["com_src"] = r.pop("companyimg__name")
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
        else:
            try:
                cursor = connection.cursor()
                cursor.execute("select distinct c.id,c.`name`,c.contact_tel,c.case_num,c.work_site_num,c.company_icon, ci.`name`  as com_src\
                    from company_companyinfo as c inner join company_companyimg as ci inner join search_price as price inner join \
                    search_style as style inner join company_companystyle as cs  \
                    on c.id=ci.company_id and c.price_id=price.id and style.id=cs.style_id and c.id=cs.company_id\
                    where (price.`name`= '{price_name}' and style.`name`='{style_name}') or (price.`name`= '{price_name}' and c.district='{district}')\
                    or (style.`name`='{style_name}' and c.district='{district}') ORDER BY c.id LIMIT {pageNum},{perPageNum}".format(
                    price_name=price,
                    style_name=style,
                    district=address,
                    pageNum=pageNum,
                    perPageNum=perPageNum))
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
