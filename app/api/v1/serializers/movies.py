from rest_framework import serializers

from app.models import Movie, Rating


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "year",
            "rate",
            "genres",
            "tags",
            "imdb_url",
            "tmdb_url",
        ]


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "year", "genres", "tags", "imdb_id", "tmdb_id"]
        read_only_fields = ["id"]


class RateSerializer(serializers.Serializer):
    rate = serializers.FloatField(min_value=1, max_value=10)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["user", "movie", "rate", "timestamp"]
        read_only_fields = ["user", "timestamp"]
