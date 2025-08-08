from django.urls import path, include
from rest_framework.routers  import DefaultRouter
from ..views import AuthorViewset

router = DefaultRouter()
router.register("", AuthorViewset, basename="author")

urlpatterns = [
    path("", include(router.urls))
]