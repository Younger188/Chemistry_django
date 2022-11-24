# coding=utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('login/', views.login_view),
    path('index/', views.index_view),
    path('upload/', views.upload_photo),
]
