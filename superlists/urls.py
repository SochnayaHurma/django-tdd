from django.urls import re_path
from lists.views import home_page

urlpatterns = [
    re_path(r'^$', home_page),
]
