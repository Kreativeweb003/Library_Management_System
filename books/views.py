from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Book, Category
from .forms import BookForm, CategoryForm


#=================================================
# Admin book list view function
#=================================================

@login_required
def book_list(request):
  
    # validating user (if it is a superuser)
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")
      
    # display all books
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


#=================================================
# Add book functionalities
#=================================================

@login_required
def add_book(request):
  
    # validating user (if it is a superuser)
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    # save bookform into a variable form 
    form = BookForm(request.POST or None)

    # Save valid form book detail
    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {'form': form})


#=================================================
# Update book functionalities
#=================================================
@login_required
def update_book(request, pk):
  
    # validating user (if it is a superuser)
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    # get book object into a book variable
    book = get_object_or_404(Book, pk=pk)

    # save BookForm in a form variable
    form = BookForm(request.POST or None, instance=book)

    # save valid form details
    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'books/book_form.html', {'form': form})


#=================================================
# Delete book functionalities
#=================================================

@login_required
def delete_book(request, pk):
  
    # validating user (if it is a superuser)
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    # get book object save into a variable (book)
    book = get_object_or_404(Book, pk=pk)

    # Delete book
    if request.method == "POST":
        book.delete()
        return redirect('book_list')

    return render(request, 'books/confirm_delete.html', {'book': book})



#=================================================
# Category liat deisplay view functionalities
#=================================================

@login_required
def category_list(request):
    
    # Validating user request
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    # Display all category objects
    categories = Category.objects.all()
  
    return render(request, 'books/category_list.html', {'categories': categories})
    
    

#=================================================
# Add category view functionalities
#=================================================
  
@login_required
def add_category(request):

    # Validating user request
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    # Saving category form into a for variables
    form = CategoryForm(request.POST or None)

    # Save for if the form is valid
    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'books/category_form.html', {'form': form})
    

#=================================================
# Update category view functionalities
#=================================================

@login_required
def update_category(request, pk):

    # Validating user request 
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    # Getting category object and save into a variable
    category = get_object_or_404(Category, pk=pk)

    # Save category form into a variable
    form = CategoryForm(request.POST or None, instance=category)

    # Save form for if it is valid
    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'books/category_form.html', {'form': form})
    

#=================================================
# Delete category view functionalities
#=================================================

@login_required
def delete_category(request, pk):

    # Validating User requests
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    # Getting category object and saved into a variable
    category = get_object_or_404(Category, pk=pk)

    # If a post request is initialized then delete category 
    if request.method == "POST":
        category.delete()
        return redirect('category_list')

    return render(request, 'books/confirm_delete_category.html', {'category': category})
    
    





