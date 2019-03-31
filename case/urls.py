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
from django.conf.urls import url, include
from . import views

app_name='case'
urlpatterns = [
    # path('admin/', views.),
    url(r'getCaseNum/',views.getCaseNum,name='getCaseNum'),
    url(r'getCase/',views.getCase,name='getCase'),
    url(r'getConditionCase/',views.getConditionCase,name='getConditionCase'),
    url(r'getConditionCaseNum/',views.getConditionCaseNum,name='getConditionCaseNum'),
    url(r'getCompanyCase/',views.getCompanyCase,name='getCompanyCase'),
    url(r'getCaseDetail/',views.getCaseDetail,name='getCaseDetail'),
    url(r'getCaseDetailImg/',views.getCaseDetailImg,name='getCaseDetailImg'),
]
