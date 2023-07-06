"""songapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import api.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', api.views.create_users),
    path('api/users/<int:user_id>/', api.views.get_user),
    path('api/songs/new/', api.views.create_song),
    path('api/songs/', api.views.list_of_songs),
    path('api/songs/<int:song_id>/', api.views.song_detail),
    path('api/update_songs/<int:song_id>/', api.views.update_song_detail),
    path('api/delete_songs/<int:song_id>/', api.views.delete_song_detail),
    path('api/create_playlist/', api.views.create_playlist),
    path('api/list_of_playlist/', api.views.list_of_playlist),
    path('api/playlist/<int:playlist_id>/', api.views.get_playlist),
    path('api/update_playlist/<int:playlist_id>/', api.views.update_playlist),
    path('api/delete_playlist/<int:playlist_id>/', api.views.delete_playlist),
    path('api/search/', api.views.search_songs),
]

