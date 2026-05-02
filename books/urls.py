from django.urls import path
from .views import (
    book_list,
    add_book,
    update_book,
    delete_book,
    # category views function
    category_list,
    add_category,
    update_category,
    delete_category
)

urlpatterns = [
    # Admin
    path('admin/books/', book_list, name='book_list'),
    path('admin/books/add/', add_book, name='add_book'),
    path('admin/books/update/<int:pk>/', update_book, name='update_book'),
    path('admin/books/delete/<int:pk>/', delete_book, name='delete_book'),
    
    # CATEGORY ROUTES
    path('admin/categories/', category_list, name='category_list'),
    path('admin/categories/add/', add_category, name='add_category'),
    path('admin/categories/update/<int:pk>/', update_category, name='update_category'),
    path('admin/categories/delete/<int:pk>/', delete_category, name='delete_category'),
    
]