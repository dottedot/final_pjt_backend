from django.contrib import admin
from .models import (
    Comments, Genres,
    Movies, Reviews,
    UserGenreMovies,
)

admin.site.register(Comments)
admin.site.register(Reviews)