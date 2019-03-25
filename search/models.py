from django.db import models

# Create your models here.

class price(models.Model):
    # 自动创建一个id列，id为主键、自增长
    name = models.CharField(max_length=30)


class renovationType(models.Model):
    # 自动创建一个id列，id为主键、自增长
    name = models.CharField(max_length=30)


class style(models.Model):
    # 自动创建一个id列，id为主键、自增长
    name = models.CharField(max_length=30)