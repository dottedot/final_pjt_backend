from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .seriaizers import (
    GenreListSerializer, 
    RecommendationListSerializer
    )
from .models import Genres, Movies

# Create your views here.

# 추천 영화 리스트
def recommendation(request):
    pass


# 인기 영화 리스트
def popular(request):
    pass


# 영화 상세 페이지
def detail(request):
    pass