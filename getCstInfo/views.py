from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
# from .serializer import SelectedSerializer, FeaturesSerializer

def getEnergy(id):
    cid = 'cd36e22dd7b74a6083da70216f22a5dc'
    secret = 'a013e69375a84d9bbb387b941aec418d'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    features = sp.audio_features(tracks=[id])
    energy = features[0]["energy"]

    energy_level = -1

    # energy{0:low, 1:middle, 2:high}
    if energy >= 0.666:
        energy_level = 2
    elif energy >= 0.400 and energy < 0.666:
        energy_level = 1
    else:
        energy_level = 0

    return energy_level

def getEmotion(id):
    cid = 'cd36e22dd7b74a6083da70216f22a5dc'
    secret = 'a013e69375a84d9bbb387b941aec418d'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    features = sp.audio_features(tracks=[id])

    energy = features[0]["energy"]
    valence = features[0]["valence"]
    emotion = -1

    # emotion{0:strong_happy, 1:week_happy, 2:week_sad, 3:strong_sad}
    if energy >= 0.5 and valence >= 0.5:
        emotion = 0
    elif energy >= 0.5 and valence < 0.5:
        emotion = 3
    elif energy < 0.5 and valence >= 0.5:
        emotion = 1
    elif energy < 0.5 and valence < 0.5:
        emotion = 2

    return emotion

def getGenre(search, date):
    words = ""
    for word in search:
        if word != ' ':
            words += word
        else:
            words += '+'

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    try:
        search_url = f"https://www.melon.com/search/total/index.htm?q={words}&section=&mwkLogType=T"
        search_data = requests.get(search_url, headers=headers)
        search_soup = BeautifulSoup(search_data.text, 'html.parser')
        for i in range(1, 6):
            search_result = search_soup.select_one(f'#frm_searchSong > div > table > tbody > tr:nth-child({i}) > td:nth-child(1) > div > input')
            song_url = f"https://www.melon.com/song/detail.htm?songId={search_result['value']}"
            song_data = requests.get(song_url, headers=headers)
            song_soup = BeautifulSoup(song_data.text, 'html.parser')
            song_result = song_soup.select_one('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)')
            melon_date = song_soup.select_one('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)')
            melon_date = melon_date.text.replace('.', '')
            spotify_date = date.replace('-', '')

            # genre{0:락/메탈, 1:발라드, 2:인디/어쿠스틱, 3:트로트, 4: 힙합/R&B 5:댄스/POP/일렉트로닉스 6:기타 7:음악찾기실패 8:에러}
            if abs(int(melon_date) - int(spotify_date)) < 2:
                genre = 6
                if '트로트' in song_result.text:
                    genre = 3
                elif '발라드' in song_result.text:
                    genre = 1
                elif '랩/힙합' in song_result.text or 'R&B/Soul' in song_result.text:
                    genre = 4
                elif '록' in song_result.text:
                    genre = 0
                elif '댄스' in song_result.text or 'POP' in song_result.text or '일렉트로니카' in song_result.text:
                    genre = 5
                elif '인디음악' in song_result.text or '포크' in song_result.text or '컨트리' in song_result.text or '블루스' in song_result.text:
                    genre = 2

                return genre
        return 7
    except:
        return 8

@csrf_exempt
def getCstInfo(request):
    received = JSONParser().parse(request)
    if request.method == 'POST':
        songData = {}
        songData['name'] = received['name']
        songData['song1'] = received['song1_id']
        songData['song2'] = received['song2_id']
        songData['song3'] = received['song3_id']
        songData['song4'] = received['song4_id']
        songData['song5'] = received['song5_id']
        # songSerializer = SelectedSerializer(data=songData)
        #
        # if songSerializer.is_valid():
        #     songSerializer.save()

        data = {}
        data['name'] = received['name']
        data['energy'] = getEnergy(received['song1_id'])
        data['emotion'] = getEmotion(received['song2_id'])

        cid = 'cd36e22dd7b74a6083da70216f22a5dc'
        secret = 'a013e69375a84d9bbb387b941aec418d'
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        song3_date = sp.track(track_id=received['song3_id'], market='KR')['album']['release_date']
        data['genre1'] = getGenre(received['song3_search'], song3_date)

        song4_date = sp.track(track_id=received['song4_id'], market='KR')['album']['release_date']
        data['genre2'] = getGenre(received['song4_search'], song4_date)

        song5_date = sp.track(track_id=received['song5_id'], market='KR')['album']['release_date']
        data['genre3'] = getGenre(received['song5_search'], song5_date)

        # cstSerializer = FeaturesSerializer(data=data)
        # if cstSerializer.is_valid():
        #     cstSerializer.save()

    return JsonResponse({'cassetti_info': data}, status=200)

