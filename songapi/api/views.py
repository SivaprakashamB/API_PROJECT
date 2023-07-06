from api.models import Song, UserProfile, Playlist
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.db.models import Q
import math

# Create your views here.

@csrf_exempt
def create_users(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name')
            gender = data.get('gender')
            age = data.get('age')

            if not name or not age:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            users = UserProfile(username=name, age=age, gender=gender)
            users.save()

            return JsonResponse({"message": "User created successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({}, status=405)


@csrf_exempt
def create_song(request):
    if request.method == "POST":
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        genre = request.POST.get('genre')
        duration = request.POST.get('duration')
        song_file = request.FILES.get('song_file')
        if not title or not artist or not genre or not duration or not song_file:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        song = Song(title=title, artist=artist, genre=genre, duration=duration)
        song.song_file = song_file
        song.save()
        return JsonResponse({"message": "Song created successfully"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def list_of_songs(request):
    if request.method == "GET":
        genre = request.GET.get('genre')
        artist = request.GET.get('artist')

        songs = Song.objects.all()

        if genre:
            songs = songs.filter(genre__icontains=genre)
        if artist:
            songs = songs.filter(artist__icontains=artist)

        # Get the page size and page number from query parameters
        page_size = int(request.GET.get('page_size', 1))  # Default to 10 songs per page
        page_number = int(request.GET.get('page', 1))  # Default to the first page

        # Calculate the start and end indexes of the songs for the requested page
        start_index = (page_number - 1) * page_size
        end_index = page_number * page_size

        # Retrieve the songs for the requested page
        paginated_songs = songs[start_index:end_index]


        songs_data = []
        for song in paginated_songs:
            song_data = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'duration': song.duration,
                'song_file': song.song_file.url,
            }
            songs_data.append(song_data)

        # Return the paginated songs data as a JSON response
        return JsonResponse({
            'songs': songs_data,
            'page': page_number,
            'total_pages': math.ceil(len(songs) / page_size)
        }, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def song_detail(request, song_id):
    if request.method == "GET":
        try:
            song = Song.objects.get(id=song_id)
            song_data = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'duration': song.duration,
                'song_file': song.song_file.url if song.song_file else None,
            }
            return JsonResponse(song_data, status=200)
        except Song.DoesNotExist:
            return JsonResponse({'error': 'Song not found'}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def update_song_detail(request, song_id):
    if request.method == "POST":
        try:
            title = request.POST.get('title')
            artist = request.POST.get('artist')
            genre = request.POST.get('genre')
            duration = request.POST.get('duration')
            song_file = request.FILES.get('song_file')

            if not title or not artist or not genre or not duration or not song_file:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            try:
                song = Song.objects.get(id=song_id)
                song.title = title
                song.artist = artist
                song.genre = genre
                song.duration = duration
                song.song_file = song_file
                song.save()
                return JsonResponse({"message": "Song updated successfully"}, status=200)
            except Song.DoesNotExist:
                return JsonResponse({"error": "Song not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_song_detail(request, song_id):
    if request.method == "DELETE":
        try:
            song = Song.objects.get(id=song_id)
            song.delete()
            return JsonResponse({"message": "Song deleted successfully"}, status=200)
        except Song.DoesNotExist:
            return JsonResponse({"error": "Song not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def create_playlist(request):
    if request.method == "POST":
        name = request.POST.get('name')
        song_ids = request.POST.get('songs')
        user_id = request.POST.get('user_id')

        if not name or not song_ids or not user_id:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        playlist = Playlist(name=name, user=user)
        playlist.save()

        song_ids = [int(song_id.strip()) for song_id in song_ids.split(',')]
        for song_id in song_ids:
            try:
                song = Song.objects.get(id=song_id)
                playlist.songs.add(song)
            except Song.DoesNotExist:
                return JsonResponse({"error": "Song not found"}, status=404)
        return JsonResponse({"message": "Playlist created successfully"}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def list_of_playlist(request):
    if request.method == "GET":
        playlists = Playlist.objects.all()

        # Get the page size and page number from query parameters
        page_size = int(request.GET.get('page_size', 1))  # Default to 10 songs per page
        page_number = int(request.GET.get('page', 1))  # Default to the first page

        # Calculate the start and end indexes of the songs for the requested page
        start_index = (page_number - 1) * page_size
        end_index = page_number * page_size

        # Retrieve the songs for the requested page
        paginated_playlists = playlists[start_index:end_index]


        playlists_data = []
        for playlist in paginated_playlists:
            playlist_data = {
                'id': playlist.id,
                'name': playlist.name,
                'user': playlist.user.username,
                'songs': [song.id for song in playlist.songs.all()],
            }
            playlists_data.append(playlist_data)

        return JsonResponse({
            'playlists': playlists_data,
            'page': page_number,
            'total_pages': math.ceil(len(playlists) / page_size)
        }, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_playlist(request, playlist_id):
    if request.method == "GET":
        try:
            playlist = Playlist.objects.get(id=playlist_id)
            playlist_data = {
                'id': playlist.id,
                'name': playlist.name,
                'user': playlist.user.username,
                'songs': [song.id for song in playlist.songs.all()],
            }
            return JsonResponse(playlist_data, status=200)
        except Playlist.DoesNotExist:
            return JsonResponse({'error': 'Playlist not found'}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def update_playlist(request, playlist_id):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            song_ids = request.POST.get('songs')
            user_id = request.POST.get('user_id')

            if not name or not song_ids or not user_id:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            try:
                playlist = Playlist.objects.get(id=playlist_id)
                playlist.name = name
                playlist.user = UserProfile.objects.get(id=user_id)
                playlist.songs.clear()
                song_ids = [int(song_id.strip()) for song_id in song_ids.split(',')]
                for song_id in song_ids:
                    try:
                        song = Song.objects.get(id=song_id)
                        playlist.songs.add(song)
                    except Song.DoesNotExist:
                        return JsonResponse({"error": "Song not found"}, status=404)

                playlist.save()
                return JsonResponse({"message": "Playlist updated successfully"}, status=200)
            except Playlist.DoesNotExist:
                return JsonResponse({'error': 'Playlist not found'}, status=404)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_playlist(request, playlist_id):
    if request.method == "DELETE":
        try:
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.delete()
            return JsonResponse({"message": "Playlist deleted successfully"}, status=200)
        except Playlist.DoesNotExist:
            return JsonResponse({"error": "Playlist not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_user(request, user_id):
    if request.method == "GET":
        try:
            user = UserProfile.objects.get(id=user_id)
            user_data = {
                'id': user.id,
                'name': user.username,
                'age': user.age,
                'gender': user.gender,
            }
            return JsonResponse(user_data, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def search_songs(request):
    if request.method == "GET":
        query = request.GET.get('q')

        if query:
            songs = Song.objects.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query) |
                Q(genre__icontains=query)
            )

            song_data = []
            for song in songs:
                song_data.append({
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'genre': song.genre,
                    'duration': song.duration,
                    'song_file': song.song_file.url if song.song_file else None
                })

            return JsonResponse({'songs': song_data}, status=200)
        else:
            return JsonResponse({'error': 'Missing search query'}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

