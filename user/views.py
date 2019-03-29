from django.shortcuts import render
from django.http import JsonResponse
import json
from . import models
from django.db import connection, connections
# 导入加密模块
from werkzeug.security import generate_password_hash, check_password_hash

# 导入my_token
from utils.my_token import *


# Create your views here.


# 用户注册
def regist(request):
    if request.method == "POST":
        # 请求方式为--POST
        try:
            # 取前端数据
            body = request.body
            user = body and json.loads(body)
            # print(user)
            if user.get('telephone') and user.get('password') and user.get('nickname'):

                # print('用户信息完整')
                # 用户信息完整
                # 查找手机号
                uu = models.userInfo.objects.filter(telephone=user['telephone']).values()
                if uu:
                    # 手机已注册-用户存在
                    return JsonResponse({"status_code": "10002", "status_text": "用户已经存在"}, safe=False)
                else:
                    # 手机尚未注册

                    # 密码加密
                    pf = generate_password_hash(user['password'], method='pbkdf2:sha1:1001', salt_length=8)
                    user['password'] = pf

                    # 注册用户
                    res_user = models.userInfo.objects.create(**user)
                    # 用户id
                    user_id = res_user.id
                    nickname = res_user.nickname

                    # 构建token
                    token = createToken(user_id)

                    return JsonResponse({"status_code": "10001", "status_text": "注册成功",
                                         "token": token, "user_id": user_id, "nickname": nickname})
            else:
                # print('用户信息错误')
                # 用户信息错误
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})

        except Exception as ex:
            print(ex)
            # 系统错误
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        # 请求方式错误
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 用户登录
def login(request):
    if request.method == "POST":
        # 请求方式为--POST
        try:
            # 取前端数据
            body = request.body
            user = body and json.loads(body)
            if user.get('telephone') and user.get('password'):
                # 用户信息完整
                # 查找用户
                res_user = list(
                    models.userInfo.objects.filter(telephone=user['telephone']).values('id', 'telephone', 'password',
                                                                                       'nickname'))
                if res_user:
                    # 用户找到
                    # 验证密码是否相同
                    if (check_password_hash(res_user[0]['password'], user['password'])):
                        # 密码正确
                        # 构建token
                        token = createToken(res_user[0]['id'])

                        return JsonResponse({"status_code": "10003", "status_text": "登录成功", "token": token,
                                             "user_id": res_user[0]['id'], "nickname": res_user[0]['nickname']})

                    else:
                        # 密码错误
                        return JsonResponse({"status_code": "10005", "status_text": "密码错误"})

                else:
                    # 未找到
                    return JsonResponse({"status_code": "10004", "status_text": "该用户不存在"})
            else:
                # 用户信息错误
                return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"})

        except Exception as ex:
            print(ex)
            # 系统错误
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        # 请求方式错误
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取用户信息
def getUserInfo(request):
    pass


# 修改用户信息
def changeUserInfo(request):
    pass


# 上传头像
def unloadImg(request):
    if request.method == "POST":
        img = json.loads(request.body)
        if img:
            img_info = models.userIcon.objects.create(**img)
            img_info.save
            if img_info:
                res = img_info.id
                return JsonResponse({"status_code": "10012", "status_text": "添加信息成功", "content": res}, safe=False)
            else:
                return JsonResponse({"status_code": "10013", "status_text": "添加信息失败"}, safe=False)
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 增加预约
def addAppointment(request):
    if request.method == "POST":
        content = json.loads(request.body)
        if content:
            appointment_id = list(models.appointment.objects.filter(company_id=content["company_id"]).values("id"))
            if appointment_id:
                return JsonResponse({"status_code": "10022", "status_text": "已经预约过了"}, safe=False)
            else:
                try:
                    appointment = models.appointment.objects.create(**content)
                    appointment.save()
                    if appointment.id:
                        return JsonResponse({"status_code": "10020", "status_text": "预约成功"}, safe=False)
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
    if request.method == "GET":
        user_id = request.GET.get("user_id")
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
    if request.method == "GET":
        appointment_id = request.GET.get("appointment_id")
        if appointment_id:
            try:
                affect_row = models.appointment.objects.filter(id=appointment_id).delete()
                if affect_row:
                    return JsonResponse({"status_code": "10023", "status_text": "取消预约成功"}, safe=False)
                else:
                    return JsonResponse({"status_code": "10023", "status_text": "取消预约失败"}, safe=False)
            except Exception as ex:
                return ex
        else:
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取验证码
def getIdentifyingCode(request):
    pass


# 修改密码接口
def updatePassword(request):
    pass


# 获取房屋信息接口
def houseList(request):
    if request.method == 'POST':
        # 请求方式为--POST
        try:
            # 取前端数据
            body = request.body
            user = body and json.loads(body)

            if user.get('user_id'):
                pass




        except Exception as ex:
            print(ex)
            # 系统错误
            return JsonResponse({"status_code": "40004", "status_text": "系统错误"})

    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 新增房屋信息
def addHouseInfo(request):
    pass


# 修改房屋信息
def updateHouseInfo(request):
    pass




# 取消预约接口
def subAppointment(request):
    pass


# 修改房屋状态接口
def updateHouse(request):
    pass


# 返回字典对象
def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
