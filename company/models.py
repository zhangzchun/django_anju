from django.db import models
from search.models import price,style

class companyInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    name = models.CharField(max_length=30)
    contact_tel = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    case_num = models.IntegerField()
    work_site_num = models.IntegerField()
    favorable_rate = models.CharField(max_length=30)
    bond = models.IntegerField()
    mouth_value = models.IntegerField()
    company_icon = models.CharField(max_length=100)
    price=models.ForeignKey(to=price,to_field="id",default=1,on_delete= models.CASCADE)

class companyImg (models.Model):
    name = models.CharField(max_length=30)
    company=models.ForeignKey(to="companyInfo",to_field="id",default=1,on_delete= models.CASCADE)

class district(models.Model):
    name = models.CharField(max_length=30)

class companyStyle(models.Model):
    company = models.ForeignKey(to="companyInfo", to_field="id", on_delete=models.CASCADE)
    style=models.ForeignKey(to=style,to_field="id", on_delete= models.CASCADE)
