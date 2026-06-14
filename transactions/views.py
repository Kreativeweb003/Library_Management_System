from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from books.models import Book
from .models import Transaction



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
        returned_at__isnull=True
    ).count()

    if active_borrows >= 5:
        messages.error(request, "You cannot borrow more than 5 books")
        return redirect('user_dashboard')

    # 3. Prevent duplicate borrow of same book
    already_borrowed = Transaction.objects.filter(
        user=request.user,
        book=book,
        returned_at__isnull=True
    ).exists()

    if already_borrowed:
        messages.error(request, "You already borrowed this book")
        return redirect('user_dashboard')

    # 4. Create transaction
    Transaction.objects.create(
        user=request.user,
        book=book
    )

    # 5. Reduce stock
    book.available_quantity -= 1
    book.save()

    messages.success(request, "Book borrowed successfully")
    return redirect('user_dashboard')




@login_required
def admin_return_book(request, transaction_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    transaction = get_object_or_404(Transaction, id=transaction_id)

    # ❌ already returned check (NEW LOGIC)
    if transaction.returned_at is not None:
        messages.error(request, "Book already returned")
        return redirect('admin_dashboard')

    # mark returned
    transaction.returned_at = timezone.now()
    transaction.save()

    # restore stock
    book = transaction.book
    book.available_quantity += 1
    book.save()

    messages.success(request, "Book marked as returned successfully")
    return redirect('admin_dashboard')



# Borrow page funtionality

@login_required
def borrowed_books(request):
    transactions = Transaction.objects.select_related('book').filter(
        user=request.user
    ).order_by('-borrowed_at')

    return render(request, 'transactions/borrowed_books.html', {
        'transactions': transactions
    })





