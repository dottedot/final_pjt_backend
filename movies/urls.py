from django.urls import path
from . import views

urlpatterns = [
    # 사용자 원하는 장르
    path('usergenre/', views.userGenre),
    
    # 추천 영화 리스트
    path('recommendation/', views.recommendation),

    # 인기 영화 리스트
    path('popular/', views.popular),

    # 영화 상세 페이지
    path('<int:movie_pk>/', views.movieDetail),


    # 영화 검색
    path('search/<str:text>/', views.search),


    # 리뷰 페이지
    path('reviews/', views.reviews),

    # 리뷰 작성페이지
    path('<int:movie_pk>/reviews/', views.makereviews),

    # 리뷰 상세 페이지
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.reviewDetail),


    # 리뷰 댓글
    path('<int:movie_pk>/reviews/<int:review_pk>/comments/', views.comments),

    # 리뷰 댓글 수정
    path(
        '<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/', 
        views.commentDetail
        ),
]
