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

app_name='search'
urlpatterns = [
    re_path(r'^searchCompany\w*/', views.searchCompany, name="searchCompany"),
    re_path(r'^searchStrategy\w*/', views.searchStrategy, name="searchStrategy"),
    re_path(r'^searchDiary\w*/', views.searchDiary, name="searchDiary"),
]
