# Generated by Django 2.1.7 on 2019-03-20 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='designerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=30)),
                ('case_num', models.IntegerField()),
                ('personal_profile', models.CharField(max_length=255)),
                ('design_concept', models.CharField(max_length=30)),
                ('grade', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.companyInfo')),
            ],
        ),
    ]