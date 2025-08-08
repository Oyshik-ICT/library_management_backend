from django.urls import path, include
from rest_framework.routers  import DefaultRouter
from ..views import BookViewset

router = DefaultRouter()
router.register("", BookViewset, basename="book")

urlpatterns = [
    path("", include(router.urls))
]