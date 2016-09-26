# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.list),
    url(r'^process/', views.process, name='process'),
]
