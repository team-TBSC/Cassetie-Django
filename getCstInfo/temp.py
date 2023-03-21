from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

def getEmotion(id):
    cid = 'cd36e22dd7b74a6083da70216f22a5dc'
    secret = 'a013e69375a84d9bbb387b941aec418d'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    name = sp.track(id)['name']
    features = sp.audio_features(tracks=[id])

    energy = features[0]["energy"]
    valence = features[0]["valence"]
    emotion = ''

    if energy >= 0.5 and valence >= 0.5:
        emotion = 'strong happy'
    elif energy >= 0.5 and valence < 0.5:
        emotion = 'strong sad'
    elif energy < 0.5 and valence >= 0.5:
        emotion = 'week happy'
    elif energy < 0.5 and valence < 0.5:
        emotion = 'week sad'

    return emotion

def getGenre(artist, track):

    try:
        api_key = '69d0593a95a68247db9ef51166d54713'
        response = requests.get(
            f'http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist={artist}&track={track}&user=kibum&format=json&api_key={api_key}')
        tags = eval(response.content.decode())['toptags']['tag']
        if (len(eval(response.content.decode())['toptags']['tag']) == 0):
            response = requests.get(
                f'http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist={artist}&user=kibum&format=json&api_key={api_key}')
            tags = eval(response.content.decode())['toptags']['tag']
    except:
        return
    result = []
    tag_result = []
    for i in range(len(tags)):
        genre = tags[i]['name'].lower()
        tag_result.append(genre)
        if "ballad" in genre or "indie" in genre or "acoustic" in genre:
            result.append('ballad')
        if "trot" in genre:
            result.append('trot')
        if "hip-hop" in genre or "rap" in genre or "r&b" in genre or "reggae" in genre:
            result.append('hiphop')
        if "rock" in genre or "metal" in genre or "punk" in genre:
            result.append('rock')
        if "k-pop" in genre or "electronic" in genre or "pop" in genre or "dance" in genre:
            result.append('dance')

    cid = 'cd36e22dd7b74a6083da70216f22a5dc'
    secret = 'a013e69375a84d9bbb387b941aec418d'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    artist_info = sp.search(q=artist, limit=1, type="artist")
    try:
        genres = artist_info['artists']['items'][0]['genres']
    except:
        return

    for i in range(len(genres)):
        genre = genres[i]
        if "ballad" in genre or "indie" in genre or "acoustic" in genre:
            result.append('ballad')
        if "trot" in genre:
            result.append('trot')
        if "hip-hop" in genre or "rap" in genre or "r&b" in genre or "reggae" in genre:
            result.append('hiphop')
        if "rock" in genre or "metal" in genre or "punk" in genre:
            result.append('rock')
        if "k-pop" in genre or "electronic" in genre or "pop" in genre or "korean pop" in genre or "dance" in genre:
            result.append('dance')

    result_genre = 'None'
    if "trot" in result:
        result_genre = 'trot'
    elif "ballad" in result:
        result_genre = 'ballad'
    elif "hiphop" in result:
        result_genre = 'hiphop'
    elif "rock" in result:
        result_genre = 'rock'
    elif "dance" in result:
        result_genre = 'dance'

    return result_genre

@csrf_exempt
def getCstInfo(request):
    received = JSONParser().parse(request)
    data = {}
    if request.method == 'POST':
        data['track'] = received['track']
        data['artist'] = received['artist']
        data['emotion'] = getEmotion(received['id'])
        data['genre'] = getGenre(received['artist'], received['track'])
        data['id'] = received['id']
    return JsonResponse({'cassetti_info': data}, status=200)
