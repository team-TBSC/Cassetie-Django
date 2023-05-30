from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def getSpotifyList(song):
    if song == '':
        return []
    cid = 'cd36e22dd7b74a6083da70216f22a5dc'
    secret = 'a013e69375a84d9bbb387b941aec418d'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    track_info = sp.search(q=song, limit=10, type="track", market='KR')
    results = []
    for i in range(len(track_info["tracks"]["items"])):
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
        results.append(result)

    return results

@csrf_exempt
def getMusicList(request):
    received = json.loads(request.body)
    if request.method == 'POST':
        data = getSpotifyList(received['track'])
        return JsonResponse({'music_list': data}, status=200)
