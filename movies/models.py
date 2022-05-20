from django.db import models

# Create your models here.


class Genres(models.Model):
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE)
    genre = models.CharField(max_length=10)


class Movies(models.Model):
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=50)
    overview = models.TextField()
    posterurl = models.TextField()
    tagline = models.TextField()
    release_date = models.TextField()
    vote_average = models.FloatField() 
    vote_count = models.IntegerField()
    runtime = models.IntegerField()