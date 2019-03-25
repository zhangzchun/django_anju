from django.db import models
from user.models import houseType
from designer.models import designerInfo
from search.models import style,renovationType

# Create your models here.


class caseInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    name = models.CharField(max_length=30)
    designer = models.ForeignKey(to=designerInfo, to_field="id" , on_delete=models.CASCADE)
    houseType = models.ForeignKey(to=houseType, to_field="id" , on_delete=models.CASCADE)
    style = models.ForeignKey(to=style, to_field="id", on_delete=models.CASCADE)
    area = models.IntegerField()
    renovationType = models.ForeignKey(to=renovationType, to_field="id", on_delete=models.CASCADE)
    cost = models.FloatField()
    duration = models.CharField(max_length=30)
    village = models.CharField(max_length=30)

class caseImg(models.Model):
    # 自动创建一个id列，id为主键、自增长
    imgType = models.ForeignKey(to="imgType", to_field="id", on_delete=models.CASCADE)
    img_url = models.CharField(max_length=255)
    case = models.ForeignKey(to="caseInfo", to_field="id", on_delete=models.CASCADE)



class imgType(models.Model):
    img_type = models.CharField(max_length=255)

