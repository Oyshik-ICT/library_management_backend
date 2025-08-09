from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .filters import BookFilter
from .models import Author, Book, Category
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer


class CategoryViewset(viewsets.ModelViewSet):
    """
    API endpoints for for managing book categories
    Only admin can create, update, delete categories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class AuthorViewset(viewsets.ModelViewSet):
    """
    API endpoints for for managing book authors
    Only admin can create, update, delete book authors
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]


class BookViewset(viewsets.ModelViewSet):
    """
    API endpoints for for managing books
    - Authenticated user can list and retrieve books
    - Only admin can create, update and delete books
    """

    queryset = Book.objects.select_related("author", "category")
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()
