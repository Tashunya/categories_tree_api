""" Categories URL Configuration"""

from django.urls import path
from categories import views

urlpatterns = [
    path('categories', views.CreateCategoryTree.as_view(),
         name='create_category_tree'),
    path("categories/<int:pk>", views.CategoryTreeDetail.as_view(),
         name="category_tree")
]
