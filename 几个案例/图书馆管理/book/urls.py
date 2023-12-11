# -*- coding: utf-8 -*-

from django.urls import path
from . import views
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

urlpatterns = [
    path("hello", views.hello),
    path("", views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('add/', views.add),
    path('select/', views.select),
    path('update/', views.update),
    path('update_confirm/', views.update_confirm),
    path('delete/<int:book_id>', views.delete),
    path('delete/', views.delete),
]
