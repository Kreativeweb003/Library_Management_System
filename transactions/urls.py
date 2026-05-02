from django.urls import path
from .views import borrow_book, return_book, borrowed_books

urlpatterns = [
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:transaction_id>/', return_book, name='return_book'),
    path('my-books/', borrowed_books, name='borrowed_books'),
]