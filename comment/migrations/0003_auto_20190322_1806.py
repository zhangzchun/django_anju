# Generated by Django 2.1.7 on 2019-03-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20190321_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentinfo',
            name='comment_time',
            field=models.DateTimeField(auto_now_add=True, max_length=0),
        ),
        migrations.AlterField(
            model_name='replyinfo',
            name='reply_time',
            field=models.DateTimeField(auto_now_add=True, max_length=0),
        ),
    ]