from django.db import models

# Create your models here.

# Create your models here.
class strategyInfo(models.Model):
    # 自动创建一个id列，id为主键、自增长
    strategy_title = models.CharField(max_length=30)
    publish_date = models.DateTimeField(auto_now_add=True,max_length=0)
    author = models.CharField(max_length=30)

class strategyContent(models.Model):
    lead = models.CharField(max_length=500)
    strategy_content = models.TextField()
    strategy = models.ForeignKey(to="strategyInfo", to_field="id", on_delete=models.CASCADE)

class strategyImg(models.Model):
    strategy_img = models.CharField(max_length=255)
    strategy = models.ForeignKey(to="strategyInfo", to_field="id", on_delete=models.CASCADE)
