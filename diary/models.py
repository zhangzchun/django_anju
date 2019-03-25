from django.db import models
from user.models import userInfo
from case.models import style, renovationType


# Create your models here.
class diaryInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    diary_title = models.CharField(max_length=30)
    publish_date = models.DateTimeField(auto_now_add=True,max_length=0)
    user = models.ForeignKey(to=userInfo, to_field="id", on_delete=models.CASCADE)
    area = models.IntegerField()
    style = models.ForeignKey(to=style, to_field="id", on_delete=models.CASCADE)
    renovationType = models.ForeignKey(to=renovationType, to_field="id", on_delete=models.CASCADE)
    village = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    browse_num = models.IntegerField()
    collect_num = models.IntegerField()
    comment_num = models.IntegerField()


class diaryContent(models.Model):
    stage = models.CharField(max_length=30)
    publish_date = models.DateField(auto_now_add=True)
    diary_content = models.CharField(max_length=500)
    diary = models.ForeignKey(to="diaryInfo", to_field="id", on_delete=models.CASCADE)

class diaryImg(models.Model):
    diary_img = models.CharField(max_length=255)
    diaryContent = models.ForeignKey(to="diaryContent", to_field="id", on_delete=models.CASCADE)
