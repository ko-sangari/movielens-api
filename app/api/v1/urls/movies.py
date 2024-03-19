from django.urls import path

from app.api.v1.views.movies import MovieListView, MovieDetailView, RateMovieView

urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("<int:id>/rate/", RateMovieView.as_view(), name="rate-movie"),
]
