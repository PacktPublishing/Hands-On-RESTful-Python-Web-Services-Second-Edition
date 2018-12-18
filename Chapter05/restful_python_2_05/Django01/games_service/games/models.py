from django.db import models


class Game(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    release_date = models.DateTimeField()
    esrb_rating = models.CharField(max_length=150)
    played_once = models.BooleanField(default=False)
    played_times = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)
