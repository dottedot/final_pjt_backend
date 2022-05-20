from django.db import models

# Create your models here.
class Genres(models.Model):
    tmdb_genre_id = models.IntegerField()
    genre = models.CharField(max_length=10)


class MovieGenre(models.Model):
    movie_fk = models.ForeignKey('Movies', on_delete=models.CASCADE)
    genre_fk = models.ForeignKey('Genres', on_delete=models.CASCADE)


class Movies(models.Model):
    genre = models.ForeignKey('Genres', on_delete=models.CASCADE)
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=50)
    overview = models.TextField()
    posterurl = models.TextField()
    tagline = models.TextField()
    release_date = models.DateTimeField(auto_now=False)
    vote_average = models.FloatField() 
    vote_count = models.IntegerField()
    runtime = models.IntegerField()