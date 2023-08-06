from django.urls import re_path, include
from lists.views import home_page

urlpatterns = [
    re_path(r'^$', home_page, name='home'),
    re_path(r'lists/', include('lists.urls')),
]

