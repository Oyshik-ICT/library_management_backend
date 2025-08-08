from rest_framework import viewsets
from .serializers import CategorySerializer, AuthorSerializer
from .models import Category, Author
from rest_framework.permissions import IsAdminUser

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]

