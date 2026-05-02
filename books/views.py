from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Book, Category
from .forms import BookForm, CategoryForm


# ADMIN ONLY: View all books
@login_required
def book_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


# CREATE
@login_required
def add_book(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    form = BookForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {'form': form})


# UPDATE
@login_required
def update_book(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {'form': form})


# DELETE
@login_required
def delete_book(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()
        return redirect('book_list')

    return render(request, 'books/confirm_delete.html', {'book': book})


#-----------------------------------
#      Category CRUD features
#------------------------------------

# Display category list
@login_required
def category_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    categories = Category.objects.all()
    return render(request, 'books/category_list.html', {'categories': categories})
    
    

# Add Category to category list
@login_required
def add_category(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'books/category_form.html', {'form': form})
    

# Update a particular category

@login_required
def update_category(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'books/category_form.html', {'form': form})
    

# Delete a particular cateagory

@login_required
def delete_category(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect('category_list')

    return render(request, 'books/confirm_delete_category.html', {'category': category})
    
    





