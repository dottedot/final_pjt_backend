from dataclasses import field
from rest_framework import serializers
from .models import Genres, Movies

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = (
            'id',
            'title',
            'posterurl',
        )


class DetailMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = (
            'id',
            'tmdb_id',
            'title',
            'overview',
            'posterurl',
            'tagline',
            'release_date',
            'vote_average',
            'vote_count',
            'runtime',
        )


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('genre',)
        