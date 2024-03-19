from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Rating


@receiver(post_save, sender=Rating)
def update_movie_rate(sender, instance, **kwargs):
    instance.movie.update_rate()
