from django.db import models
from company.models import companyInfo
# Create your models here.

class designerInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    icon = models.CharField(max_length=255)
    name = models.CharField(max_length=30)
    case_num = models.IntegerField()
    personal_profile = models.CharField(max_length=255)
    design_concept = models.CharField(max_length=250)
    grade = models.CharField(max_length=30)
    company = models.ForeignKey(to=companyInfo, to_field="id", on_delete=models.CASCADE)
