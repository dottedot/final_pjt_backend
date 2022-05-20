from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .seriaizers import (
    GenreListSerializer, 
    MovieListSerializer,
    DetailMovieListSerializer,
    )
from .models import Genres, Movies

# Create your views here.

# 추천 영화 리스트
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def recommendation(request):
    pass


# 인기 영화 리스트
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def popular(request):
    pass


# 영화 상세 페이지
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def detail(request, movie_pk):
    movie = Movies.objects.get(id=movie_pk)
    genres = Genres.objects.filter(movie_id=movie_pk)
    movie_serializer = DetailMovieListSerializer(movie)
    genre_serializer = GenreListSerializer(genres, many=True)
    serializer = movie_serializer.data
    serializer['genres'] = genre_serializer.data

    return Response(serializer, status=status.HTTP_200_OK)
