from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.v1.serializers.movies import (
    MovieSerializer,
    MovieCreateSerializer,
    RateSerializer,
    RatingSerializer,
)
from app.models import Movie, Rating
from app.paginations import MoviesPagination


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Movie data.

    Supports listing, creating, retrieving, updating, and deleting movies.
    Allows searching by title and filtering by tags and genres.
    Uses different serializers for listing and creating movies.
    Authentication varies based on action (GET: None, Others: Required).
    """

    queryset = Movie.objects.all().order_by("title")
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]
    filterset_fields = ["tags", "genres"]
    pagination_class = MoviesPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Depending on the request method, different serializers are used.
        """
        if self.action == "list" or self.action == "retrieve":
            return MovieSerializer
        return MovieCreateSerializer

    @swagger_auto_schema(
        request_body=RatingSerializer,
        responses={
            200: openapi.Response("Movie rated successfully"),
            400: "Invalid input",
            404: "Movie not found",
        },
        operation_description="Rate a movie. Users can submit a rating for a given movie.",
        operation_summary="Rate a Movie",
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="rate",
    )
    def rate(self, request, pk=None):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            rating_value = serializer.validated_data["rate"]

            try:
                movie = Movie.objects.get(id=pk)
                rating = Rating.objects.create(
                    user=request.user, movie=movie, rate=rating_value
                )
                return Response(
                    RatingSerializer(rating).data, status=status.HTTP_200_OK
                )
            except Movie.DoesNotExist:
                return Response(
                    {"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND
                )
            except IntegrityError:
                return Response(
                    {"error": "You have already rated this movie"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
