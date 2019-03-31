from django.shortcuts import render
from django.http import JsonResponse
import json
from . import models
from django.db import connection, connections
import random

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
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                cursor = connection.cursor()
                sql = "select `user`.nickname,`user`.id,`user`.telephone,icon.icon,sex.gender as sex,`user`.QQ,`user`.address\
                        from user_userinfo as `user` INNER JOIN user_usericon as icon INNER JOIN user_sex as sex\
                        on `user`.userIcon_id=icon.id  and `user`.sex_id=sex.id\
                        WHERE `user`.id={user_id}".format(user_id=user_id)
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


# 修改用户信息
def changeUserInfo(request):
    if request.method == 'POST':
    # # 请求方式为--POST
        try:
            # 取前端数据
            # body = request.body
            # user = body and json.loads(body)
            user_info=json.loads(request.body)
            print(user_info)
            if user_info:
                sex=list(models.sex.objects.filter(gender=user_info["sex"]).values("id"))
                del user_info["sex"]

                user_info["six_id"]=sex[0]["id"]
                print(user_info)
                # row=models.userInfo.objects.filter(id=user_info["id"]).update(nickname=user_info["nickname"],
                # QQ=user_info["QQ"],six_id=user_info["six_id"],address=user_info["address"])
                # house_status=userInfo["house_status"],houseType_id=userInfo["houseType_id"])

                user=models.userInfo.objects.create(**user_info)
                user.save()
                print(user)
                if user:
                    return JsonResponse({"status_code": "10014", "status_text": "更新信息成功"}, safe=False)
                else:
                    return JsonResponse({"status_code": "10015", "status_text": "更新信息失败"}, safe=False)
        except Exception as ex:
            return ex
        # 系统错误
        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)



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
    if request.method == 'GET':
        id = random.choice(range(1, 3))
        if id:
            try:
                res=list(models.identifyingCode.objects.filter(id=id).values())
                if res:
                    print(res)
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": res}, safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                return ex

    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 修改密码接口
def updatePassword(request):
    if request.method == 'POST':
    # # 请求方式为--POST
        try:
            # 取前端数据
            # body = request.body
            # user = body and json.loads(body)
            passWord=json.loads(request.body)
            print(passWord)
            if passWord:
                oldPwd=list(models.userInfo.objects.filter(id=passWord["id"]).values("password"))
                print(oldPwd)
                if (check_password_hash(oldPwd[0]['password'], passWord['old_pwd'])):
                    pf = generate_password_hash(passWord['new_pwd'], method='pbkdf2:sha1:1001', salt_length=8)
                    passWord['new_pwd'] = pf
                    row=models.userInfo.objects.filter(id=passWord["id"]).update(password=passWord['new_pwd'])
                    if row:
                        return JsonResponse({"status_code": "10014", "status_text": "更新信息成功"})
                    else:
                        return JsonResponse({"status_code": "10015", "status_text": "更新信息失败"})

                else:
                    return JsonResponse({"status_code": "10005", "status_text": "密码错误"})

        except Exception as ex:
            return ex
        # 系统错误
        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)


# 获取房屋信息接口
def getHouseList(request):
    if request.method == 'GET':
        # 请求方式为--GET
        # 取前端数据
        user_id = request.GET.get("user_id")
        house_id= request.GET.get("house_id")
        # user["house_id"]:
        if house_id:
            # house_id
            try:
                res = models.houseInfo.objects.filter(id=house_id).values("id",
                                                                           "name",
                                                                           "houseType__name",
                                                                           "area",
                                                                           "house_status",
                                                                           "address",
                                                                           "village"
                                                                            )
                houseinfo = list(res)
                if houseinfo:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": houseinfo},
                                        safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
                # 系统错误
                return JsonResponse({"status_code": "40004", "status_text": "系统错误"})

        elif user_id:
            # print("这里")
            try:
                res = models.houseInfo.objects.filter(user_id=user_id).values("id",
                                                                               "name",
                                                                               "houseType__name",
                                                                               "area",
                                                                               "house_status",
                                                                               "address",
                                                                                "village"
                                                                                )

                houselist = list(res)
                if houselist:
                    return JsonResponse({"status_code": "10009", "status_text": "找到数据", "content": houselist},
                                        safe=False)
                else:
                    return JsonResponse({"status_code": "10008", "status_text": "未找到数据"}, safe=False)
            except Exception as ex:
                print(ex)
                # 系统错误
                return JsonResponse({"status_code": "40004", "status_text": "系统错误"}, safe=False)

        else:
            # 信息错误
            return JsonResponse({"status_code": "40005", "status_text": "数据格式不合法"}, safe=False)

    else:
        # 请求方式错误
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)



# 更新房屋信息
def updateHouseInfo(request):
    if request.method == 'POST':
    # # 请求方式为--POST
        try:
            # 取前端数据
            # body = request.body
            # user = body and json.loads(body)
            houseInfo=json.loads(request.body)
            print(houseInfo)
            if houseInfo:
                del houseInfo["flag"]
                houseType=list(models.houseType.objects.filter(name=houseInfo["type"]).values("id"))
                del houseInfo["type"]
                houseInfo["houseType_id"]=houseType[0]["id"]
                row=models.houseInfo.objects.filter(id=houseInfo["id"]).update(name=houseInfo["name"],
                area=houseInfo["area"],village=houseInfo["village"],address=houseInfo["address"],
                house_status=houseInfo["house_status"],houseType_id=houseInfo["houseType_id"])

                # house=models.houseInfo.objects.filter(id=houseInfo["id"])
                # house.update()
                print(row)
                if row:
                    return JsonResponse({"status_code": "10014", "status_text": "更新信息成功"}, safe=False)
                else:
                    return JsonResponse({"status_code": "10015", "status_text": "更新信息失败"}, safe=False)
        except Exception as ex:
            return ex
        # 系统错误
        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 新增房屋信息
def addHouseInfo(request):
    if request.method == 'POST':
    # # 请求方式为--POST
        try:
            houseInfo=json.loads(request.body)
            print(houseInfo)
            if houseInfo:
                del houseInfo["flag"]
                houseType=list(models.houseType.objects.filter(name=houseInfo["type"]).values("id"))
                del houseInfo["type"]
                houseInfo["houseType_id"]=houseType[0]["id"]
                print(houseInfo)
                house=models.houseInfo.objects.create(**houseInfo)
                house.save()
                if house.id:
                    return JsonResponse({"status_code": "10012", "status_text": "添加信息成功"}, safe=False)
                else:
                    return JsonResponse({"status_code": "10013", "status_text": "添加信息失败"}, safe=False)
        except Exception as ex:
            return ex
        # 系统错误
        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
    else:
        return JsonResponse({"status_code": "40006", "status_text": "请求方式错误"}, safe=False)

# 删除房屋信息
def delHouseInfo(request):
    if request.method == 'POST':
    # # 请求方式为--POST
        try:
            house_id=json.loads(request.body)
            print(house_id["id"])
            if house_id["id"]:

                row=models.houseInfo.objects.filter(id=house_id["id"]).delete()
                print(row)
                if row:
                    return JsonResponse({"status_code": "10016", "status_text": "删除信息成功"}, safe=False)
                else:
                    return JsonResponse({"status_code": "10017", "status_text": "删除信息失败"}, safe=False)
        except Exception as ex:
            return ex
        # 系统错误
        return JsonResponse({"status_code": "40004", "status_text": "系统错误"})
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
