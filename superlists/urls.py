from django.contrib import admin
from django.urls import path, re_path
from lists.views import home_page

urlpatterns = [
    re_path(r'^$', home_page),
]
