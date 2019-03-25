from django.db import models
from user.models import userInfo


# Create your models here.
class commentInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    fromu = models.ForeignKey(to=userInfo, to_field="id", on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=500)
    comment_time = models.DateTimeField(auto_now_add=True,max_length=0)
    commentType = models.ForeignKey(to="commentType", to_field="id", on_delete=models.CASCADE)
    comment_obj_id = models.IntegerField()
    comment_num = models.IntegerField(default=0)


class commentType(models.Model):
    # 自动创建一个id列，id为主键、自增长
    comment_type = models.CharField(max_length=30)


class replyInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    fromu = models.ForeignKey(to=userInfo, to_field="id",on_delete=models.CASCADE)
    comment = models.ForeignKey(to="commentInfo", to_field="id", null=True, on_delete=models.CASCADE)
    reply = models.ForeignKey(to="replyInfo", to_field="id",default=None, null=True, on_delete=models.CASCADE)
    replyType = models.ForeignKey(to="replyType", to_field="id", on_delete=models.CASCADE)
    reply_content = models.CharField(max_length=500)
    tou_id = models.IntegerField()
    tou_nickname = models.CharField(max_length=30)
    reply_time = models.DateTimeField(auto_now_add=True,max_length=0)


class replyType(models.Model):
    # 自动创建一个id列，id为主键、自增长
    reply_type = models.CharField(max_length=30)
