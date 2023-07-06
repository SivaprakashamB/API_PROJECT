from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    song_file = models.FileField(upload_to='songs/')

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, related_name='playlists')


