from dataclasses import field
from rest_framework import serializers
from .models import Genres, Movies

class RecommendationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        field = (
            'id',
            'title',
            'posterurl',
        )

class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        field = ('genre')
        