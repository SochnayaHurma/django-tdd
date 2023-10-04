from django.urls import re_path

from .views import new_list, view_list, my_lists


urlpatterns = [
    re_path(r'^new$', new_list, name='new-list'),
    re_path(r'^(\d+)/$', view_list, name='unique-list'),
    re_path(r'^users/([a-z0-9@.]+)/$', my_lists, name="my-lists")
]
