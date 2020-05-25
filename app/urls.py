from django.urls import path, include
from django.conf.urls import re_path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from app import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
routers=DefaultRouter()
routers.register("",views.JianchengViewsSet)

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path("table_ajax/", include(routers.urls)),
]