from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import RegisterForm
from books.models import Book
from transactions.models import Transaction


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to access this page")
        
    books = Book.objects.all()

    return render(request, 'accounts/admin_dashboard.html')


@login_required
def user_dashboard(request):
    query = request.GET.get('q')

    books = Book.objects.filter(available_quantity__gt=0)

    if query:
        books = books.filter(title__icontains=query)

    borrowed_books = Transaction.objects.filter(
        user=request.user,
        is_returned=False
    )

    context = {
        'books': books,
        'borrowed_books': borrowed_books
    }

    return render(request, 'accounts/user_dashboard.html', context)