# Generated by Django 2.1.7 on 2019-03-22 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20190322_2229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='replyinfo',
            old_name='tou',
            new_name='tou_id',
        ),
    ]