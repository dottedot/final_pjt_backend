from rest_framework import serializers

from .models import (
    Genres, 
    Movies, 
    Reviews, 
    Comments
    )


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


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = (
            'id',
            'title',
            'content',
            'score',
            'created_at',
            'updated_at',
            )


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            'id',
            'content',
            'created_at',
            'updated_at',
            )


class ReviewSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = (
            'title',
            'content',
            'score',
            'created_at',
            'updated_at',
            )


class CommentSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            'content',
            'created_at',
            'updated_at',
            )