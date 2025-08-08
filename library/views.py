from rest_framework import viewsets
from .serializers import CategorySerializer, AuthorSerializer, BookSerializer
from .models import Category, Author, Book
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]

class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author", "category")
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

