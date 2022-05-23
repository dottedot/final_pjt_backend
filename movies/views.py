from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import Genres, Movies, Reviews
from .serializers import (
    GenreListSerializer, 
    MovieListSerializer,
    DetailMovieListSerializer,
    ReviewListSerializer,
    CommentListSerializer,
    ReviewSaveSerializer,
    CommentSaveSerializer,
    )
from dj_rest_auth.serializers import TokenSerializer
User = get_user_model()

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
@permission_classes([IsAuthenticated])
def movieDetail(request, movie_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)
    genres = Genres.objects.filter(movie=movie_pk)

    movie_serializer = DetailMovieListSerializer(movie)
    genre_serializer = GenreListSerializer(genres, many=True)

    serializer = movie_serializer.data
    serializer['genres'] = genre_serializer.data

    return Response(serializer, status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reviews(request, movie_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)

    if request.method == 'GET':
        reviews = Reviews.objects.filter(movie=movie)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        serializer = ReviewSaveSerializer(data=request.data)
        review = Reviews.objects.filter(user=user, movie=movie)
        
        # 내가 리뷰를 이전에 작성했을 때
        if len(review) > 0:
            data = {
                'result': f'리뷰를 이미 작성하셨습니다.'
            }
            return Response(data, status=status.HTTP_208_ALREADY_REPORTED)

        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def reviewDetail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)
    review = Reviews.objects.get(pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewListSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        data = {
            'result': f'{review_pk} 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        user = User.objects.get(pk=request.user.id)
        serializer = ReviewSaveSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comments(request, movie_pk, review_pk):
    pass



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def commentDetail(request, movie_pk, review_pk, comment_pk):
    pass