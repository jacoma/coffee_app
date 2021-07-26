# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 21:15:46 2021

@author: jacoma
"""
from django.urls import path
from polls import views

urlpatterns = [
    path("", views.index, name="index"),
]