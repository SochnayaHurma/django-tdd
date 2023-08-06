from django.urls import re_path

from .views import new_list, view_list, add_item


urlpatterns = [
    re_path(r'^new$', new_list, name='new-list'),
    re_path(r'^(\d+)/$', view_list, name='unique-list'),
    re_path(r'(\d+)/add_item$', add_item, name="add-item"),
]
