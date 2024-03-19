from django.contrib import admin

from app.models import Movie, Rating


class MovieAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("id", "title", "year", "rate")


admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating)
