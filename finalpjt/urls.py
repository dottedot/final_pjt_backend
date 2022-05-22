from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/accounts/', include('dj_rest_auth.urls')),
    path('api/v1/accounts/registration/', include('dj_rest_auth.registration.urls')),
    
    path('api/v1/movies/', include('movies.urls')),
]
