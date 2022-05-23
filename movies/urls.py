from django.urls import path
from . import views

urlpatterns = [
    # 추천 영화 리스트
    path('recommendation/', views.recommendation),

    # 인기 영화 리스트
    path('popular/', views.popular),

    # 영화 상세 페이지
    path('<int:movie_pk>/', views.movieDetail),


    # 리뷰 페이지
    path(
        '<int:movie_pk>/reviews/', 
        views.reviews
        ),

    # 리뷰 상세 페이지
    path(
        '<int:movie_pk>/reviews/<int:review_pk>/', 
        views.reviewDetail
        ),


    # 리뷰 댓글
    path(
        '<int:movie_pk>/reviews/<int:review_pk>/comments/', 
        views.comments
        ),

    # 리뷰 댓글 수정
    path(
        '<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/', 
        views.commentDetail
        ),
]
