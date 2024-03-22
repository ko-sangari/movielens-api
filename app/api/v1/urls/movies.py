from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.api.v1.views.movies import MovieViewSet


router = DefaultRouter()
router.register("", MovieViewSet, basename="movie")

urlpatterns = [
    path("", include(router.urls)),
]
