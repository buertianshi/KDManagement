"""KDManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import views
from . import search2
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login',views.login),
    url(r'^search-post$',search2.search_post),
    url(r'^sign$',views.sign,name='sign'),
    url(r'^login',views.login,name='login'),
    url(r'^personInfo',views.personInfo,name='personInfo'),
    url(r'^complaint$',views.complaint,name='complaint'),
    url(r'^addKD$',views.addKD,name='addKD'),
    url(r'^$',views.mainpage),
    url(r'^userMain$',views.userMain,name='userMain'),
    url(r'^kdyMain$',views.kdyMain,name='kdyMain'),
    url(r'^searchKD$',views.searchKD,name='searchKD'),
    url(r'^searchKDbyusername$',views.searchKDbyusername,name='searchKDbyusername'),
    url(r'^adminMain$',views.adminMain,name='adminMain'),
    url(r'^updateKD$',views.updateKD,name='updateKD'),
    url(r'^addKDY$',views.addKDY,name='addKDY'),
    url(r'^addNetwork$',views.addNetwork,name='addNetwork'),
    url(r'^deleteNetwork$',views.deleteNetwork,name='deleteNetwork'),
    url(r'^queryNetwork$',views.queryNetwork,name='queryNetwork'),
    url(r'^updateKDY$',views.updateKDY,name='updateKDY'),
    url(r'^superadminMain$',views.superadminMain,name='superadminMain'),
    url(r'^addAdmin$',views.addAdmin,name='addAdmin'),
    url(r'^updateAdmin$',views.updateAdmin,name='updateAdmin'),
    url(r'^handleComplaint$',views.handleComplaint,name='handleComplaint'),
]
