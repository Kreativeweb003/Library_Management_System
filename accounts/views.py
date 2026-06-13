from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import RegisterForm
from books.models import Book
from transactions.models import Transaction
from django.contrib.auth.models import User





#==========================================
#  User Registeration Functionalities
#==========================================



def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # email check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        user.save()

        messages.success(request, "Account created successfully. You can now log in.")
        return redirect("login")

    return render(request, "accounts/register.html")


#=================================================
#  Login to Admin / User Dashboard Funtionalities
#=================================================


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


#==========================================
#  Admin Dashboard Functionalities
#==========================================


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to access this page")
        
    books = Book.objects.all()

    return render(request, 'accounts/admin_dashboard.html')


#==========================================
#  User Dashboard Functionalities
#==========================================


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

#==========================================
#  Logout Funtionalities
#==========================================


def logout_view(request):
    logout(request)
    return redirect('login')

