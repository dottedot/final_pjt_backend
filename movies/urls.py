from django.urls import path
from . import views

urlpatterns = [
    # 추천 영화 리스트
    path('recommendation/', views.recommendation),

    # 인기 영화 리스트
    path('popular/', views.popular),

    # 영화 상세 페이지
    path('<int:movie_pk>/', views.detail),
]
