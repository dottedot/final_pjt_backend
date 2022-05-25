from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Genres, Movies,
    Reviews, Comments,
    UserGenreMovies,
    )
from .serializers import (
    GenreListSerializer, MovieListSerializer, DetailMovieListSerializer,
    ReviewListSerializer, CommentListSerializer,
    ReviewSaveSerializer, CommentSaveSerializer,
    UserGenreSerializer,
    )

User = get_user_model()

def get_cvector_genres():
    N = 250
    movies = Movies.objects.order_by('-vote_average')[:N]
    data=[]
    for i in range(N):
        genres = Genres.objects.filter(movie=movies[i])
        genre_str = ' '.join([genre.genre for genre in genres])
        data.append([
            movies[i].tmdb_id, genre_str, 
            movies[i].vote_average, 
            movies[i].vote_count])

    df = pd.DataFrame(
        data,
        columns=[
            'tmdb_id', 'genres', 
            'vote_average', 'vote_count'
            ]
        )

    m = df['vote_count'].quantile(1)
    C = df['vote_average'].mean()

    def weightd_rating(x, m=m, C=C):
        v=x['vote_count']
        R=x['vote_average']
        return (v/(v+m+R)+(m/(m+v)*C))

    df['score'] = df.apply(weightd_rating, axis=1)
    
    count_vector = CountVectorizer(ngram_range=(1,3))
    cvector_genres = count_vector.fit_transform(df['genres'])
    return cvector_genres, df


cvector_genres, df = get_cvector_genres()


# 추천 영화 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation(request):
    # 선택한 장르가 우선 (리뷰개수가 1단위면 그대로, 10단위면*5 100단위면*10 해서 가중치)
    # 리뷰작성한거의 장르를 가지고 총 가중치를 구해서 정렬한다.
    # 이거를 추천함수에 넣는다.

    user_review = Reviews.objects.filter(user=request.user)
    user_genre = UserGenreMovies.objects.get(user=request.user)
        
    if not user_review:
        recommend = []
        movies = Genres.objects.filter(genre=user_genre.genre1)[:20]
        for movie in movies:
            m = Movies.objects.get(pk=movie.movie_id).vote_average
            recommend.append([movie.movie_id, m])
        movies = Genres.objects.filter(genre=user_genre.genre2)[:20]
        for movie in movies:
            m = Movies.objects.get(pk=movie.movie_id).vote_average
            recommend.append([movie.movie_id, m])
        movies = Genres.objects.filter(genre=user_genre.genre3)[:20]
        for movie in movies:
            m = Movies.objects.get(pk=movie.movie_id).vote_average
            recommend.append([movie.movie_id, m])
        
        recommend.sort(key = lambda x:-x[1])

        if len(recommend) > 20:
            recommend = recommend[:20]

    else:
        genre_c_sim = cosine_similarity(cvector_genres, cvector_genres).argsort()[:,::-1]
        print(genre_c_sim)
        def get_recommend_movie_list(df, top=30):
            sim_index = genre_c_sim[user_review[0].movie.id, :top].reshape(-1)
            result = df.iloc[sim_index].sort_values('score', ascending=False)[:40]
            
            for review in user_review[1:]:
                sim_index = genre_c_sim[review.movie.id, :top].reshape(-1)
                data = df.iloc[sim_index].sort_values('score', ascending=False)[:20]
                print(result)
                print(data)
                result = pd.concat(result, data)
            # result.sort_values('score', ascending=False)

            result = result.drop_duplicates(['tmdb_id']).sort_values('score', ascending=False)[:20]
            result = result.values.tolist()
            return result
        recommend = get_recommend_movie_list(df)

    data = []

    for reco in recommend:
        # if type(reco)
        if len(reco) == 2:
            movie = Movies.objects.get(pk=reco[0])
        else:
            movie = Movies.objects.get(tmdb_id=reco[0])
        data.append({
            'tmdb_id': movie.tmdb_id,
            'title': movie.title,
            'posterurl': movie.posterurl,
        })

    return Response(data, status=status.HTTP_200_OK)



# 시작시 사용자 장르 선택
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def userGenre(request):
    if request.method == 'GET':
        user_genre = UserGenreMovies.objects.filter(user=request.user)
        if len(user_genre) > 0:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            genres = Genres.objects.filter().values('genre').distinct()
            return Response(genres, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        serializer = UserGenreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# 인기 영화 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def popular(request):
    movies = Movies.objects.order_by('-vote_average')[:20]
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