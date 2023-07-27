from django.urls import re_path
from lists.views import home_page, view_list

urlpatterns = [
    re_path(r'^$', home_page, name='home'),
    re_path(r'^lists/ed-v-mire-spisok/$', view_list, name='unique-list'),
]
