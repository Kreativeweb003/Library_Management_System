from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from books.models import Book
from .models import Transaction


# ✅ BORROW BOOK
@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # 1. Check availability
    if book.available_quantity <= 0:
        messages.error(request, "Book not available")
        return redirect('user_dashboard')

    # 2. Check user limit (max 5 active books)
    active_borrows = Transaction.objects.filter(
        user=request.user,
        is_returned=False
    ).count()

    if active_borrows >= 5:
        messages.error(request, "You cannot borrow more than 5 books")
        return redirect('user_dashboard')

    # 3. Prevent duplicate borrow of same book
    already_borrowed = Transaction.objects.filter(
        user=request.user,
        book=book,
        is_returned=False
    ).exists()

    if already_borrowed:
        messages.error(request, "You already borrowed this book")
        return redirect('user_dashboard')

    # 4. Create transaction
    Transaction.objects.create(
        user=request.user,
        book=book
    )

    # 5. Reduce available quantity
    book.available_quantity -= 1
    book.save()

    messages.success(request, "Book borrowed successfully")
    return redirect('user_dashboard')


# ✅ RETURN BOOK
@login_required
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if transaction.is_returned:
        messages.error(request, "Book already returned")
        return redirect('user_dashboard')

    # Mark as returned
    transaction.is_returned = True
    transaction.returned_at = timezone.now()
    transaction.save()

    # Increase available quantity
    book = transaction.book
    book.available_quantity += 1
    book.save()

    messages.success(request, "Book returned successfully")
    return redirect('user_dashboard')


# Borrow page funtionality
@login_required
def borrowed_books(request):
    transactions = Transaction.objects.filter(
        user=request.user,
        is_returned=False
    )

    return render(request, 'transactions/borrowed_books.html', {
        'transactions': transactions
    })




