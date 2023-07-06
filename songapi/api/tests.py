from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Song, Playlist, UserProfile
import json

class CreateSongTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_song(self):
        # Path to the song file
        song_file_path = 'E:/song/songs/first.mpeg'

        # Open the song file and read its contents
        with open(song_file_path, 'rb') as f:
            file_content = f.read()

        # Create a SimpleUploadedFile instance with the file content and content type
        file = SimpleUploadedFile(
            name='first.mpeg',
            content=file_content,
            content_type='audio/mpeg'
        )

        data = {
            'title': 'Song Title',
            'artist': 'Artist Name',
            'genre': 'Pop',
            'duration': 3,
            'song_file': file,
        }

        response = self.client.post('/api/songs/new/', data, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Song.objects.count(), 1)
        song = Song.objects.first()
        self.assertEqual(song.title, 'Song Title')
        self.assertEqual(song.artist, 'Artist Name')
        self.assertEqual(song.genre, 'Pop')
        self.assertEqual(song.duration, 3)

    def test_retrieve_song(self):
        # Create a song in the database
        song = Song.objects.create(
            title='Song Title',
            artist='Artist Name',
            genre='Pop',
            duration=3,
            song_file='first.mpeg'
        )

        # Send a GET request to retrieve the song
        response = self.client.get(f'/api/songs/2/')

        self.assertEqual(response.status_code, 200)

        # Parse the response JSON data
        song_data = response.json()

        # Assert the retrieved song data
        self.assertEqual(song_data['title'], 'Song Title')
        self.assertEqual(song_data['artist'], 'Artist Name')
        self.assertEqual(song_data['genre'], 'Pop')
        self.assertEqual(song_data['duration'], 3)

    def test_update_song(self):
        # Path to the song file
        song_file_path = 'E:/song/songs/first.mpeg'

        # Open the song file and read its contents
        with open(song_file_path, 'rb') as f:
            file_content = f.read()

        # Create a SimpleUploadedFile instance with the file content and content type
        file = SimpleUploadedFile(
            name='first.mpeg',
            content=file_content,
            content_type='audio/mpeg'
        )

        song = Song.objects.create(
            title='Song Title',
            artist='Artist Name',
            genre='Pop',
            duration=3,
            song_file=file,
        )
        response = self.client.post(f'/api/update_songs/3/', {
            'title': 'Updated Song Title',
            'artist': 'Updated Artist Name',
            'genre': 'Rock',
            'duration': 4,
            'song_file': file,
        })
        self.assertEqual(response.status_code, 200)
        song.refresh_from_db()
        self.assertEqual(song.title, 'Updated Song Title')
        self.assertEqual(song.artist, 'Updated Artist Name')

    def test_delete_song(self):
        # Path to the song file
        song_file_path = 'E:/song/songs/first.mpeg'

        # Open the song file and read its contents
        with open(song_file_path, 'rb') as f:
            file_content = f.read()

        # Create a SimpleUploadedFile instance with the file content and content type
        file = SimpleUploadedFile(
            name='first.mpeg',
            content=file_content,
            content_type='audio/mpeg'
        )
        song = Song.objects.create(
            title='Song Title',
            artist='Artist Name',
            genre='Pop',
            duration=3,
            song_file=file,
        )
        response = self.client.post(f'/api/delete_songs/2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Song.objects.count(), 0)

    def test_add_song_to_playlist(self):
        # Path to the song file
        song_file_path = 'E:/song/songs/first.mpeg'

        # Open the song file and read its contents
        with open(song_file_path, 'rb') as f:
            file_content = f.read()

        # Create a SimpleUploadedFile instance with the file content and content type
        file = SimpleUploadedFile(
            name='first.mpeg',
            content=file_content,
            content_type='audio/mpeg'
        )

        # Create a song in the database
        song = Song.objects.create(
            title='Song Title',
            artist='Artist Name',
            genre='Pop',
            duration=3,
            song_file=file
        )

        # Create a user profile
        user_profile = UserProfile.objects.create(username='tester', age=12, gender='male')

        # Create a playlist in the database
        playlist = Playlist.objects.create(name='My Playlist', user=user_profile)

        # Add the song to the playlist
        playlist.songs.set([song])

        # Update the name of the playlist
        playlist.name = 'Updated Song'
        playlist.save()

        # Retrieve the updated playlist from the API
        response = self.client.post('/api/create_playlist/', {
            'name': 'Updated Song',
            'songs': '1',
            'user_id': '1',
        })

        self.assertEqual(response.status_code, 201)

        # Parse the response JSON data
        playlist_data = response.json()

        # Assert that the song is present in the playlist
        self.assertEqual(playlist.name, 'Updated Song')

    def test_list_of_playlist(self):
        # Create playlists in the database
        user_profile = UserProfile.objects.create(username='tester', age=12, gender='male')
        playlist1 = Playlist.objects.create(name='Playlist 1', user_id=user_profile.id)

        # Send a GET request to the view
        response = self.client.get('/api/list_of_playlist/')

        self.assertEqual(response.status_code, 200)

        # Parse the response JSON data
        data = response.json()
        print("data", data)
        # Assert the expected number of playlists
        self.assertEqual(len(data['playlists']), 1)

        # Assert the playlist data
        self.assertEqual(data['playlists'][0]['name'], 'Playlist 1')

    def test_update_playlist(self):
        # Path to the song file
        song_file_path = 'E:/song/songs/first.mpeg'

        # Open the song file and read its contents
        with open(song_file_path, 'rb') as f:
            file_content = f.read()

        # Create a SimpleUploadedFile instance with the file content and content type
        file = SimpleUploadedFile(
            name='first.mpeg',
            content=file_content,
            content_type='audio/mpeg'
        )

        song = Song.objects.create(
            title='Song Title',
            artist='Artist Name',
            genre='Pop',
            duration=3,
            song_file=file,
        )
        # Create a user profile
        user_profile = UserProfile.objects.create(username='tester', age=12, gender='male')

        # Create a playlist in the database
        playlist = Playlist.objects.create(name='Playlist 1', user=user_profile)
        print("playlistplaylistplaylistplaylist", playlist.id)
        # Send a POST request to update the playlist
        response = self.client.post(f'/api/update_playlist/1/', {
            'name': 'Updated Playlist',
            'songs': '1',
            'user_id': user_profile.id,
        })

        self.assertEqual(response.status_code, 200)

        # Retrieve the updated playlist from the database
        updated_playlist = Playlist.objects.get(id=playlist.id)

        # Assert the updated playlist data
        self.assertEqual(updated_playlist.name, 'Updated Playlist')
        self.assertEqual(list(updated_playlist.songs.values_list('id', flat=True)), [1])

    def test_delete_playlist(self):
        # Create a playlist in the database
        playlist = Playlist.objects.create(name='Playlist 1', user_id=1)

        # Send a DELETE request to delete the playlist
        response = self.client.delete(f'/api/delete_playlist/1/')

        self.assertEqual(response.status_code, 200)

        # Assert that the playlist is deleted
        self.assertFalse(Playlist.objects.filter(id=playlist.id).exists())




