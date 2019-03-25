"""django_anju URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from . import views

app_name='diary'
urlpatterns = [
    re_path(r'^diaryList\w*/',views.diaryList,name="diaryList"),
    re_path(r'^diaryDetailHeader\w*/',views.diaryDetailHeader,name="diaryDetailHeader"),
    re_path(r'^diaryDetailContent\w*/',views.diaryDetailContent,name="diaryDetailContent"),
    re_path(r'^diaryUserIcon\w*/',views.diaryUserIcon,name="diaryUserIcon"),
    re_path(r'^indexDiary\w*/',views.indexDiary,name="indexDiary"),
    re_path(r'^diaryTitle\w*/',views.diaryTitle,name="diaryTitle"),
    re_path(r'^writeDiary\w*/',views.writeDiary,name="writeDiary"),
]
