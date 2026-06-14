from django.urls import path
from .views import (
    borrow_book,
    borrowed_books,
    admin_return_book,
)

urlpatterns = [
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('my-books/', borrowed_books, name='borrowed_books'),

    path('admin-return/<int:transaction_id>/', admin_return_book, name='admin_return_book'),
]