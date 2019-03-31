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
from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('regist/', views.regist, name='regist'),

    path('changeUserInfo/', views.changeUserInfo, name='changeUserInfo'),
    path('getIdentifyingCode/', views.getIdentifyingCode, name='getIdentifyingCode'),
    path('updatePassword/', views.updatePassword, name='updatePassword'),
    path('getUserInfo/', views.getUserInfo, name='getUserInfo'),
    path('getHouseList/', views.getHouseList, name='getHouseList'),
    path('addHouseInfo/', views.addHouseInfo, name='addHouseInfo'),
    path('updateHouseInfo/', views.updateHouseInfo, name='updateHouseInfo'),
    path('delHouseInfo/', views.delHouseInfo, name='delHouseInfo'),

    path('addAppointment/', views.addAppointment, name='addAppointment'),
    path('getAppointment/', views.getAppointment, name='getAppointment'),
    path('cancelAppointment/', views.cancelAppointment, name='cancelAppointment'),
    path('unloadImg/', views.unloadImg, name='unloadImg')
]
