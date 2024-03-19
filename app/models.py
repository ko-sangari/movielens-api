from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField(default=0)
    rate = models.FloatField(default=0.0, editable=False)
    genres = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=1000, blank=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    tmdb_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ("title", "year")

    def imdb_url(self):
        if self.imdb_id:
            return f"http://www.imdb.com/title/tt{self.imdb_id}/"
        return None

    def tmdb_url(self):
        if self.tmdb_id:
            return f"https://www.themoviedb.org/movie/{self.tmdb_id}"
        return None

    def __str__(self):
        return f"{self.title} ({self.year})"

    def update_rate(self):
        total_rating = sum(rating.rate for rating in self.rating_set.all())
        self.rate = total_rating / self.rating_set.count()
        self.save()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} rating for {self.movie.title}: {self.rating}"
