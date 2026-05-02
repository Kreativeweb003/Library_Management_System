from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')

    quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()

    publication_year = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure available_quantity never exceeds quantity
        if self.available_quantity > self.quantity:
            self.available_quantity = self.quantity

        # If creating a new book, set available_quantity = quantity
        if not self.pk:
            self.available_quantity = self.quantity

        super().save(*args, **kwargs)