from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from library.models import Book
from .models import Borrow
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.db import transaction
from .serializers import BorrowSerializer

class BorrowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if "book_id" not in request.data:
            return Response(
                {"details": "Book id is needed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        book_id = request.data.get("book_id")
        user = request.user

        with transaction.atomic():
            book = get_object_or_404(Book.objects.select_for_update(), pk=book_id)

            if not book.is_available():
                return Response(
                    {"details": "Book  is not available"},
                    status=status.HTTP_400_BAD_REQUEST
            )
            if Borrow.objects.filter(user=user, return_date__isnull=True).count() >= 3:
                return Response(
                    {"details": "You can't borrow more than 3 books"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            Borrow.objects.create(
                user = user,
                book = book,
                due_date = date.today() + timedelta(days=14)
            )

            book.decrement_copies()

            return Response(
                    {"details": "Borrowing book is successful"},
                    status=status.HTTP_201_CREATED
                )

    def get(self, request):
        borrows = Borrow.objects.filter(user = request.user, return_date__isnull=True)
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)
    
class ReturnBookViewset(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if "borrow_id" not in request.data:
            return Response(
                {"details": "Borrow id is needed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        borrow_id = request.data.get("borrow_id")
        user = request.user
        
        with transaction.atomic():
            try:
                borrow = Borrow.objects.select_related("book").select_for_update().get(borrow_id=borrow_id, user=user, return_date__isnull=True)
            except Borrow.DoesNotExist:
                return Response(
                    {"details": "Invalid borrow record or book already returned"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            borrow.return_date = date.today()
            borrow.save(update_fields=["return_date"])

            borrow.book.increment_copies()

            if borrow.is_overdue():
                penalty_points = borrow.days_late()
                user.penalty_points += penalty_points
                user.save(update_fields=["penalty_points"])

            return Response(
                    {"details": "Book returns succesfully"},
                    status=status.HTTP_200_OK
                )



