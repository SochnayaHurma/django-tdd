from django.urls import re_path
from lists.views import home_page, view_list, new_list

urlpatterns = [
    re_path(r'^$', home_page, name='home'),
    re_path(r'^lists/(.+)/$', view_list, name='unique-list'),
    re_path(r'^lists/new$', new_list, name='new-list'),
]
