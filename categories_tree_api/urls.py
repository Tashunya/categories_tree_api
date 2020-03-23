"""
categories_tree_api URL Configuration
"""

from django.contrib import admin
from django.urls import re_path, include


urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^', include('categories.urls')),
]
