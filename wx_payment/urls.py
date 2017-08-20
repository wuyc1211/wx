"""wx_payment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
# from rest_framework import routers
from payment.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^wx/get-token/$', getToken),
    url(r'^wx/create-order/$', CreateOrderView.as_view()),
    
    url(r'^wx/users/$', WxUserList.as_view()),
    url(r'^wx/users/(?P<pk>[0-9]+)/$', WxUserDetail.as_view()),
    
    url(r'^wx/orders/$', OrderList.as_view()),
    url(r'^wx/orders/(?P<pk>[0-9]+)/$', OrderDetail.as_view()),
    
    url(r'^wx/orders/(?P<order_id>[0-9]+)/data-list/$', OrderDataList.as_view()),
    url(r'^wx/orders/(?P<order_id>[0-9]+)/data-list/(?P<pk>[0-9]+)/$', OrderDataDetail.as_view()),
]

