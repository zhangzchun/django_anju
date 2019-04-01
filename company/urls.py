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
from . import views
from django.urls import path, re_path

app_name='commpany'
urlpatterns = [
    # re_path(r'^companyList\w*/',views.companyList,name="companyList"),
    re_path(r'^indexCompanyList\w*/',views.indexCompanyList,name="indexCompanyList"),
    re_path(r'^companyDetail\w*/',views.companyDetail,name="companyDetail"),
    re_path(r'^companySort\w*/',views.companySort,name="companySort"),
    # re_path(r'^companyScreen\w*/',views.companyScreen,name="companyScreen")

    re_path(r'^companyList\w*/', views.companyList, name="companyList"),
    re_path(r'^companyNum\w*/', views.companyNum, name="companyNum"),
    re_path(r'^getConditionCompany\w*/', views.getConditionCompany, name="getConditionCompany"),
    re_path(r'^getConditionComNum\w*/', views.getConditionComNum, name="getConditionComNum"),
    re_path(r'^indexCompanyList\w*/', views.indexCompanyList, name="indexCompanyList")
]
