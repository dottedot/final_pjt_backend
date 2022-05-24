import requests

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalpjt.settings")
import django
django.setup()
from movies.models import Genres, Movies


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


def get_movie():
    BASE_URL = 'http://api.themoviedb.org/3'
    params = {
        'api_key' : '7c999d7887b2a767b982be9183549dc1',
        'region' : 'KR',
        'language' : 'ko'
    }
    check = [
        'title', 'overview','poster_path','tagline', 'genres',
        'release_date','vote_average','vote_count','runtime'
        ]
        
    last_movie = get_last_movie()
    now_id = last_movie.id
    now_tmdb_id = last_movie.tmdb_id
    
    for tmdb_id in range(now_tmdb_id+1, 88888):
        
        path = f'/movie/{tmdb_id}'
        response = requests.get(BASE_URL+path, params=params)
        data = response.json()

        if 'success' in data.keys(): 
            # id에 해당하는 영화가 없다
            continue
        else:
            movie = {}
            for key in check:
                # data 들의 key에 해당하는 값이 하나라도 없으면 거른다.
                if key not in data.keys():
                    break
                if not data[key]:
                    break

                # 모든 key들이 정상적으로 존재한다면 정제 시작.
                movie[key] = data[key]
            else:
                Movies(
                    title=movie['title'],
                    overview=movie['overview'],
                    posterurl='https://image.tmdb.org/t/p/original'+movie['poster_path'],
                    tagline=movie['tagline'],
                    release_date=movie['release_date'],
                    vote_average=movie['vote_average'],
                    vote_count=movie['vote_count'],
                    runtime=movie['runtime'],
                    tmdb_id=tmdb_id,
                    ).save()

                now_id += 1
                print(f'save id: {now_id}, {tmdb_id}, {movie["title"]}')
                
                for g in data['genres']:
                    Genres(
                        movie=Movies.objects.get(id=now_id), 
                        genre=g['name']
                        ).save()
    # print(data)

def get_last_movie():
    movies = Movies.objects.all()
    return Movies.objects.get(id=len(movies))


if __name__=='__main__':
    get_movie()