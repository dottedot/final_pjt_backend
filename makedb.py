import requests

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalpjt.settings")
import django
django.setup()
from movies.models import Genres


def get_tmdb_genres():
    BASE_URL = 'http://api.themoviedb.org/3'
    path = '/genre/movie/list'
    params = {
        'api_key' : '7c999d7887b2a767b982be9183549dc1',
        'region' : 'KR',
        'language' : 'ko'
    }
    response = requests.get(BASE_URL+path, params=params)
    data = response.json()

    return data['genres']


if __name__=='__main__':
    genres_dict = get_tmdb_genres()

    for genre in genres_dict:
        Genres(tmdb_genre_id=genre['id'], genre=genre['name']).save()