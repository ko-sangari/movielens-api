from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework import generics
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


class MovieListView(generics.ListCreateAPIView):
    """
    List and create movies.

    Provides functionality to retrieve a list of movies with optional search and
    filter capabilities, as well as to create new movie entries.

    Methods
    -------
    GET:
        Returns a list of movies. Supports filtering by `tags` and `genres` and
        searching by movie `title`.
        Authentication is not required.

    POST:
        Creates a new movie entry.
        Authentication is required.

    Search Fields
    -------------
    title: str
        The title of the movie to search for.

    Filter Fields
    -------------
    tags: str
        Comma-separated tags to filter movies by.
    genres: str
        Comma-separated genres to filter movies by.
    """

    queryset = Movie.objects.all().order_by("title")
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]
    filterset_fields = ["tags", "genres"]
    pagination_class = MoviesPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MovieSerializer
        return MovieCreateSerializer


class MovieDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a movie's details.

    Provides functionality to retrieve detailed information about a specific movie
    and to update the details of an existing movie.

    Methods
    -------
    GET:
        Returns detailed information about a specific movie.
        Authentication is not required.

    PUT/PATCH:
        Updates the details of a specific movie.
        Authentication is required.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]


class RateMovieView(APIView):
    """
    Submit a rating for a specific movie.

    Allows authenticated users to rate a movie. Each user can submit only one
    rating per movie.

    Methods
    -------
    POST:
        Submits a new rating for a movie.
        Requires the authenticated user to provide a rating value.
        Returns an error if the user has already rated the specific movie.

    Parameters
    ----------
    id : int
        The unique identifier of the movie to be rated.
    rate : float
        The rating value given by the user.

    Returns
    -------
    HTTP 200 OK:
        On successful rating submission.
    HTTP 400 Bad Request:
        If invalid data is provided or the user has already rated the movie.
    HTTP 404 Not Found:
        If the specified movie does not exist.
    """

    permission_classes = [IsAuthenticated]

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
    def post(self, request, id):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            rating_value = serializer.validated_data["rate"]

            try:
                movie = Movie.objects.get(pk=id)
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
