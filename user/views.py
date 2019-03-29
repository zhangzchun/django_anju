from django.shortcuts import render
from django.http import JsonResponse
import json
from . import models
from django.db import connection, connections

# Create your views here.

# 增加预约
def addAppointment(request):
    if request.method=="POST":
        content=json.loads(request.body)
        if content:
            appointment_id=list(models.appointment.objects.filter(company_id=content["company_id"]).values("id"))
            if appointment_id:
                return JsonResponse({"status_code": "10022", "status_text": "已经预约过了"}, safe=False)
            else:
                try:
                    appointment=models.appointment.objects.create(**content)
                    appointment.save()
                    if appointment.id:
                        return JsonResponse({"status_code":"10020","status_text":"预约成功"}, safe=False)
                    else:
                        return JsonResponse({"status_code": "10021", "status_text": "预约失败"}, safe=False)
                except Exception as ex:
                    print(ex)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 获取预约
def getAppointment(request):
    if request.method=="GET":
        user_id=request.GET.get("user_id")
        if user_id:
            try:
                cursor = connection.cursor()
                sql = "SELECT a.id, c.company_icon, c.`name` company_name, c.case_num, c.work_site_num, c.contact_tel, \
                        hy.`name` house_type, h.area, h.address, h.village, a.appointment_status\
                        from user_appointment a INNER JOIN company_companyinfo c INNER JOIN user_houseinfo h \
                        INNER JOIN user_housetype hy ON a.company_id=c.id and a.house_id=h.id and h.houseType_id=hy.id\
                        where a.user_id={user_id}".format(user_id=user_id)
                cursor.execute(sql)
                res = dictfetchall(cursor)
                if res:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 取消预约
def cancelAppointment(request):
    if request.method=="GET":
        appointment_id=request.GET.get("appointment_id")
        if appointment_id:
            try:
                affect_row = models.appointment.objects.filter(id=appointment_id).delete()
                if affect_row:
                    return JsonResponse({"status_code":"10023","status_text":"取消预约成功"}, safe=False)
                else:
                    return JsonResponse({"status_code":"10023","status_text":"取消预约失败"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 上传头像
def unloadImg(request):
    if  request.method=="POST":
        img=json.loads(request.body)
        if img:
            img_info=models.userIcon.objects.create(**img)
            img_info.save
            if img_info:
                res=img_info.id
                return JsonResponse({"status_code": "10012", "status_text": "添加信息成功", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10013", "status_text": "添加信息失败"}, safe=False)
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