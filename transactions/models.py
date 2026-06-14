from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
  
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"