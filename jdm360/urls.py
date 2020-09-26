from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('services',views.services),
    path('register', views.register),
    path('login', views.login),
    path('logout',views.logout),
    path('order', views.order),
    path('placeorder', views.placeorder),
    path('admin', views.admin),
    path('client', views.client),
    path('aboutus', views.aboutus),
    path('completed/<int:order_id>', views.completed),
    path('edit/<int:order_id>', views.edit),
    path('view/<int:order_id>', views.view),
    path('photographer/<int:user_id>', views.photographer),
    path('updateorder/<int:order_id>', views.updateorder),
    path('assign/<int:order_id>', views.assign),
    path('loginreg', views.loginreg),
    path('makeadmin/<int:user_id>', views.makeadmin),
    path('makeclient/<int:user_id>', views.makeclient),
    path('deleteorder/<int:order_id>', views.deleteorder),
    path('payorder/<int:order_id>', views.payorder),
    path('open/<int:order_id>', views.openorder),
    path('photographerpage', views.photopage),
]