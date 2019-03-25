from django.db import models
from user.models import userInfo


# Create your models here.

class collectInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    content_id = models.IntegerField()
    collectType = models.ForeignKey(to="collectType", to_field="id", on_delete=models.CASCADE)
    user = models.ForeignKey(to=userInfo, to_field="id", on_delete=models.CASCADE)
    collect_date = models.DateField(auto_now_add=True, null=True)


class collectType(models.Model):
    # 自动创建一个id列，id为主键、自增长
    name = models.CharField(max_length=30)
