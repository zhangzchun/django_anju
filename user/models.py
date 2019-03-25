from django.db import models
from company.models import companyInfo

# Create your models here.
class userInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    telephone = models.CharField(unique=True, max_length=30)
    nickname = models.CharField(max_length=30)
    sex = models.ForeignKey(to="sex", to_field="id", default=1, null=True, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    userIcon = models.ForeignKey(to="userIcon", to_field="id", default=1, null=True, on_delete=models.CASCADE)
    QQ = models.CharField(max_length=30, null=True, )
    address = models.CharField(max_length=30, null=True, )
    regist_data = models.DateTimeField(auto_now_add=True,max_length=0)


class userIcon(models.Model):
    # 自动创建一个id列，id为主键、自增长
    icon = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True,max_length=0)


class sex(models.Model):
    gender = models.CharField(max_length=30)


class identifyingCode(models.Model):
    url_code = models.CharField(max_length=255)
    code_content = models.CharField(max_length=255)


class houseInfo(models.Model):
    name = models.CharField(max_length=30, null=True)
    houseType = models.ForeignKey(to="houseType", to_field="id", null=True, on_delete=models.CASCADE)
    area = models.IntegerField()
    village = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30)
    house_status = models.CharField(max_length=30)
    user = models.ForeignKey(to="userInfo", to_field="id", on_delete=models.CASCADE)


class houseType(models.Model):
    name = models.CharField(max_length=30, null=True)


class appointment(models.Model):
    # 自动创建一个id列，id为主键、自增长
    house = models.ForeignKey(to="houseInfo", to_field="id", on_delete=models.CASCADE)
    company = models.ForeignKey(to=companyInfo, to_field="id", on_delete=models.CASCADE)
    appointment_status = models.CharField(max_length=30, default="正在预约")
    user = models.ForeignKey(to="userInfo", to_field="id", on_delete=models.CASCADE)
