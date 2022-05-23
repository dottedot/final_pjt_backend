from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Genres, Movies,
    Reviews, Comments,
    )
from .serializers import (
    GenreListSerializer, MovieListSerializer, DetailMovieListSerializer,
    ReviewListSerializer, CommentListSerializer,
    ReviewSaveSerializer, CommentSaveSerializer,
    )
from movies import serializers

User = get_user_model()


# 추천 영화 리스트
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def recommendation(request):
    pass



# 인기 영화 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def popular(request):
    movies = Movies.objects.order_by('vote_average')[:20]
    serializer = MovieListSerializer(movies, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)



# 영화 상세 페이지
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movieDetail(request, movie_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)
    genres = Genres.objects.filter(movie=movie_pk)

    # 영화와 장르 합쳐서 데이터 전달
    movie_serializer = DetailMovieListSerializer(movie)
    genre_serializer = GenreListSerializer(genres, many=True)
    serializer = movie_serializer.data
    serializer['genres'] = genre_serializer.data

    return Response(serializer, status=status.HTTP_200_OK)



# 전체 리뷰 보여주거나 리뷰 처음 작성하는 페이지
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reviews(request, movie_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)

    # GET Method
    if request.method == 'GET':
        reviews = Reviews.objects.filter(movie=movie)
        serializer = ReviewListSerializer(reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST Method
    elif request.method == 'POST':
        '''
        작동 과정
        1. 내가 리뷰를 작성했었다면 작성하지 못하도록 메시지를 보낸다
        2. 처음 리뷰를 작성한다면 리뷰를 작성하도록 한다.
        3. movie의 vote 관련해서 처리를 해준다.(사람수 증가, 투표 평균 수정)
        '''
        
        user = User.objects.get(pk=request.user.id)
        serializer = ReviewSaveSerializer(data=request.data)
        review = Reviews.objects.filter(user=user, movie=movie)
        
        # 1. 내가 리뷰를 작성했었다면 작성하지 못하도록 메시지를 보낸다
        if len(review) > 0:
            data = {
                'result': f'리뷰를 이미 작성하셨습니다.'
            }
            return Response(data, status=status.HTTP_208_ALREADY_REPORTED)

        # 2. 처음 리뷰를 작성한다면 리뷰를 작성하도록 한다.
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)

            # 3. movie의 vote 관련해서 처리를 해준다.(사람수 증가, 투표 평균 수정)
            v_avg, v_cnt = movie.vote_average, movie.vote_count
            v_avg = ((v_avg * v_cnt) + int(serializer.data['score'])) / (v_cnt + 1)
            v_avg = round(v_avg, 1)
            v_cnt = f'{int(v_cnt) - 1}'
            movie.vote_average, movie.vote_count = v_avg, v_cnt
            movie.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)



# 내가 작성한 리뷰 보기/수정/삭제
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def reviewDetail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)
    review = Reviews.objects.get(pk=review_pk)

    # GET Method
    if request.method == 'GET':
        serializer = ReviewListSerializer(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE Method
    elif request.method == 'DELETE':
        '''
        작동 과정
        1. movie의 vote 관련해서 처리를 해준다.(사람수 감소, 투표 평균 수정)
        2. 리뷰를 삭제한다
        '''

        # 1. movie의 vote 관련해서 처리를 해준다.(사람수 감소, 투표 평균 수정)
        v_avg, v_cnt = movie.vote_average, movie.vote_count
        v_avg = (((v_avg * v_cnt) - int(review.score)) / (v_cnt - 1))
        v_avg = round(v_avg, 1)
        v_cnt = f'{int(v_cnt) - 1}'
        movie.vote_average, movie.vote_count = v_avg, v_cnt
        movie.save()

        # 2. 리뷰를 삭제한다
        review.delete()
        data = {
            'result': f'{review_pk} 삭제되었습니다.'
        }

        return Response(data, status=status.HTTP_204_NO_CONTENT)

    # PUT Method
    elif request.method == 'PUT':
        user = User.objects.get(pk=request.user.id)
        serializer = ReviewSaveSerializer(data=request.data, instance=review)

        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



# 전체 댓글을 보여주기 / 댓글 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comments(request, movie_pk, review_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)
    review = get_object_or_404(Reviews, pk=review_pk)

    # GET Method
    if request.method == 'GET':
        comments = Comments.objects.filter(movie=movie, review=review_pk)
        serializer = CommentListSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST Method
    elif request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        serializer = CommentSaveSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user, review=review)

            return Response(serializer.data, status=status.HTTP_201_CREATED)



# 내가 작성한 댓글 수정/삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def commentDetail(request, movie_pk, review_pk, comment_pk):
    movie = get_object_or_404(Movies, tmdb_id=movie_pk)
    review = get_object_or_404(Reviews, pk=review_pk)
    comment = Comments.objects.get(pk=comment_pk)

    # DELETE Method
    if request.method == 'DELETE':
        comment.delete()
        data = { 'result': f'{comment_pk} 삭제되었습니다.' }

        return Response(data, status=status.HTTP_204_NO_CONTENT)

    # PUT Method
    elif request.method == 'PUT':
        user = User.objects.get(pk=request.user.id)
        serializer = CommentSaveSerializer(data=request.data, instance=comment)

        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user, review=review)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)