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
from django.urls import path,re_path
from . import views

app_name='collect'
urlpatterns = [
    re_path(r'^increaseCollection\w*/',views.increaseCollection,name="increaseCollection"),
    re_path(r'^cancelCollection\w*/',views.cancelCollection,name="cancelCollection"),
    re_path(r'^checkCollection\w*/',views.checkCollection,name="checkCollection"),
    re_path(r'^diaryCollections\w*/',views.diaryCollections,name="diaryCollections"),
    re_path(r'^strategyCollections\w*/',views.strategyCollections,name="strategyCollections"),
    re_path(r'^companyCollections\w*/',views.companyCollections,name="companyCollections"),
    re_path(r'^caseCollections\w*/',views.caseCollections,name="caseCollections")
]
