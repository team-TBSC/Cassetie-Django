from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def getSpotifyList(song):
    cid = 'cd36e22dd7b74a6083da70216f22a5dc'
    secret = 'a013e69375a84d9bbb387b941aec418d'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    track_info = sp.search(q=song, limit=10, type="track", market='KR')
    results = {}
    for i in range(10):
        name = track_info["tracks"]["items"][i]['name']
        artist = track_info["tracks"]["items"][i]['artists'][0]['name']
        album = track_info["tracks"]["items"][i]['album']['name']
        image = track_info["tracks"]["items"][i]['album']['images'][0]['url']
        # spotify_url = track_info["tracks"]["items"][i]['external_urls']['spotify']
        preview_url = track_info["tracks"]["items"][i]['preview_url']
        id = track_info["tracks"]["items"][i]['id']

        result = {"track": name,
                  "artist": artist,
                  "album": album,
                  "image": image,
                  # "spotify_url": spotify_url,
                  "preview_url": preview_url,
                  "id": id,
                  }
        results[i] = result

    return results

@csrf_exempt
def getMusicList(request):
    received = JSONParser().parse(request)
    if request.method == 'POST':
        data = getSpotifyList(received['track'])
    return JsonResponse({'music_list': data}, status=200)