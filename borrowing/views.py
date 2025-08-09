import logging
import uuid
from datetime import date, timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import Book
from user.models import CustomUser

from .models import Borrow
from .serializers import BorrowSerializer

logger = logging.getLogger(__name__)


class BorrowView(APIView):
    """
    API endpoint to borrow a book
    - Users can borrow at max 3 books at a time
    - Locks the book record to avoid race condition
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if "book_id" not in request.data:
                return Response(
                    {"details": "Book id is needed"}, status=status.HTTP_400_BAD_REQUEST
                )
            book_id = request.data.get("book_id")
            user = request.user

            with transaction.atomic():
                book = get_object_or_404(Book.objects.select_for_update(), pk=book_id)

                if not book.is_available():
                    return Response(
                        {"details": "Book  is not available"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if (
                    Borrow.objects.filter(user=user, return_date__isnull=True).count()
                    >= 3
                ):
                    return Response(
                        {"details": "You can't borrow more than 3 books"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                Borrow.objects.create(
                    user=user, book=book, due_date=date.today() + timedelta(days=14)
                )

                book.decrement_copies()

                return Response(
                    {"details": "Borrowing book is successful"},
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            logger.error(f"Error in borrowing book=> {e}", exc_info=True)
            return Response(
                {"details": "An error occure while borrowing the book"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        """
        Retrieve a list of currently borrowed books for the authenticated user
        """
        try:
            borrows = Borrow.objects.filter(user=request.user, return_date__isnull=True)
            serializer = BorrowSerializer(borrows, many=True)

            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving borrowed books=> {e}", exc_info=True)
            return Response(
                {"details": "An error occure while retrieving borrowed books"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReturnBookViewset(APIView):
    """
    API endpoint for returning borrowd book
    - Update penalty points if the book is overdue
    """

    permission_classes = [IsAuthenticated]

    def is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def post(self, request):
        try:
            if "borrow_id" not in request.data:
                return Response(
                    {"details": "Borrow id is needed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            borrow_id = request.data.get("borrow_id")

            if not self.is_valid_uuid(borrow_id):
                return Response(
                    {"details": "Invalid borrow_id. Need valid UUID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = request.user

            with transaction.atomic():
                try:
                    borrow = (
                        Borrow.objects.select_related("book")
                        .select_for_update()
                        .get(borrow_id=borrow_id, user=user, return_date__isnull=True)
                    )
                except Borrow.DoesNotExist:
                    return Response(
                        {"details": "Invalid borrow record or book already returned"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                borrow.return_date = date.today()
                borrow.save(update_fields=["return_date"])

                borrow.book.increment_copies()

                if borrow.is_overdue():
                    penalty_points = borrow.days_late()
                    user.penalty_points += penalty_points
                    user.save(update_fields=["penalty_points"])

                return Response(
                    {"details": "Book returns successfully"}, status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Error in returning book=> {e}", exc_info=True)
            return Response(
                {"details": "An error occure while returning borrowed book"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserPenaltyPointsView(APIView):
    """
    API endpoint to check penalty points for a user
    - User can view their own penalty points
    - Staff cab view any user's penalty points
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            current_user = request.user
            try:
                target_user = CustomUser.objects.get(pk=id)
            except CustomUser.DoesNotExist:
                return Response(
                    {"details": "User doesn't exit"}, status=status.HTTP_404_NOT_FOUND
                )

            if current_user.is_staff or target_user == current_user:
                return Response(
                    {
                        "details": f"Total penalty points of {target_user.username} is {target_user.penalty_points}"
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"details": "You don't have permission to do this"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            logger.error(f"Error in retrieving penalty points=> {e}", exc_info=True)
            return Response(
                {"details": "An error occure while retrieving penalty points"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
