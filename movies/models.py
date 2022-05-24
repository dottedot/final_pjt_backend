from django.db import models
from django.conf import settings

# Create your models here.

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


class Genres(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    genre = models.CharField(max_length=10)



class Reviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserGenreMovies(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre1 = models.CharField(max_length=10)
    genre2 = models.CharField(max_length=10)
    genre3 = models.CharField(max_length=10)