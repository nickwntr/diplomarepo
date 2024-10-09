"""
URL configuration for siteproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from distutils.dep_util import newer
from tkinter.font import names

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from siteapp.views import *

app_name = 'siteapp'

urlpatterns = [
    path('', start),
    path('admin/', admin.site.urls),
    path('about/', about),
    path('shop/',eshop),
    path('shop/additem', nitemview, name='nitemview'),
    path('shop/additem/new', newitem, name='newitem'),
    path('login/',login,name='login'),
    path('login/reg/', regview, name='regview'),
    path('login/reg/newuser',newuser,name='newuser'),
    path('login/unlog',unlogin, name='unlogin'),
    path('contacts/',conts),
    path('cart/', cart_detail,name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='cart_add'),
    path('cart/item_clear/<int:product_id>/', remove_from_cart, name='item_clear'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_item'),
    path('cart/checkout', make_order, name='make_order')
]
