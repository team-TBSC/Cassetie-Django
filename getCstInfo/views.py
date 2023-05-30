# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
from .serializer import SelectedSerializer
from getCstInfo.models import Selected
import random

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
    if energy >= 0.65 and valence >= 0.5:
        emotion = 0
    elif energy >= 0.55 and valence < 0.5:
        emotion = 3
    elif energy < 0.65 and valence >= 0.5:
        emotion = 1
    elif energy < 0.55 and valence < 0.5:
        emotion = 2

    return emotion

def selectGenre(text):
    # genre{0:락/메탈, 1:발라드, 2:인디/어쿠스틱, 3:트로트, 4: 힙합/R&B 5:댄스일렉트로닉스 6:POP 7:기타 8:음악찾기실패 9:에러}
    if '트로트' in text:
        return 3
    elif '발라드' in text:
        return 1
    elif '댄스' in text:
        return 5
    elif '인디' in text or '포크' in text:
        return 2
    elif '랩' in text or 'R&B' in text:
        return 4
    elif '록' in text:
        return 0
    elif 'POP' in text or '일렉트로니카' in text:
        return 6
    elif '컨트리' in text or '블루스' in text:
        return 2
    else:
        return 7

def getGenre(id, search):
    cid = 'cd36e22dd7b74a6083da70216f22a5dc'
    secret = 'a013e69375a84d9bbb387b941aec418d'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    spotify_date = sp.track(track_id=id)['album']['release_date']
    spotify_date = spotify_date.replace('-', '')

    album_name = sp.track(track_id=id)['album']['name']
    words = ""
    for word in album_name:
        if word != ' ':
            words += word
        else:
            words += '+'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    search_url = f"https://www.melon.com/search/total/index.htm?q={words}&section=&mwkLogType=T"
    search_data = requests.get(search_url, headers=headers)
    search_soup = BeautifulSoup(search_data.text, 'html.parser')
    try:
        melon_date = search_soup.select_one('#frm > div > ul >  div > div > dl > dd.wrap_btn > span.cnt_view')
        melon_date = melon_date.text.replace('.', '')
        search_result = search_soup.select_one('#frm > div > ul > div > div > dl > dd.wrap_btn > a')
        song_url = f"https://www.melon.com/album/detail.htm?albumId={search_result['data-album-no']}"
        song_data = requests.get(song_url, headers=headers)
        song_soup = BeautifulSoup(song_data.text, 'html.parser')
        song_result = song_soup.select_one(
            '#conts > div.section_info > div > div.entry > div.meta > dl > dd:nth-child(4)').text
        print(song_result)

        if abs(int(melon_date) - int(spotify_date)) < 5:
            return selectGenre(song_result)
    except:
        print("no one album")
        pass

    for i in range(1, 4):
        try:
            melon_date = search_soup.select_one(
                f'#frm > div > ul > li:nth-child({i}) > div > div > dl > dd.wrap_btn > span.cnt_view')
            melon_date = melon_date.text.replace('.', '')
            spotify_date = spotify_date.replace('-', '')
            search_result = search_soup.select_one(
                f'#frm > div > ul > li:nth-child({i}) > div > div > dl > dd.wrap_btn > a')
            song_url = f"https://www.melon.com/album/detail.htm?albumId={search_result['data-album-no']}"
            song_data = requests.get(song_url, headers=headers)
            song_soup = BeautifulSoup(song_data.text, 'html.parser')
            song_result = song_soup.select_one(
                '#conts > div.section_info > div > div.entry > div.meta > dl > dd:nth-child(4)').text

            if abs(int(melon_date) - int(spotify_date)) < 5:
                return selectGenre(song_result)
        except:
            print("no album")
            break

    track_name = sp.track(track_id=id)['name']
    words = ""
    for word in track_name:
        if word != ' ':
            words += word
        else:
            words += '+'

    search_url = f"https://www.melon.com/search/total/index.htm?q={words}&section=&mwkLogType=T"
    search_data = requests.get(search_url, headers=headers)
    search_soup = BeautifulSoup(search_data.text, 'html.parser')
    for i in range(1, 6):
        try:
            search_result = search_soup.select_one(
                f'#frm_searchSong > div > table > tbody > tr:nth-child({i}) > td:nth-child(1) > div > input')
            song_url = f"https://www.melon.com/song/detail.htm?songId={search_result['value']}"
            song_data = requests.get(song_url, headers=headers)
            song_soup = BeautifulSoup(song_data.text, 'html.parser')
            song_result = song_soup.select_one(
                '#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)').text
            melon_date = song_soup.select_one('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)')
            melon_date = melon_date.text.replace('.', '')

            if abs(int(melon_date) - int(spotify_date)) < 5:
                return selectGenre(song_result)
        except:
            print("no song")
            break

    words = ""
    for word in search:
        if word != ' ':
            words += word
        else:
            words += '+'

    search_url = f"https://www.melon.com/search/total/index.htm?q={words}&section=&mwkLogType=T"
    search_data = requests.get(search_url, headers=headers)
    search_soup = BeautifulSoup(search_data.text, 'html.parser')
    for i in range(1, 6):
        try:
            search_result = search_soup.select_one(
                f'#frm_searchSong > div > table > tbody > tr:nth-child({i}) > td:nth-child(1) > div > input')
            song_url = f"https://www.melon.com/song/detail.htm?songId={search_result['value']}"
            song_data = requests.get(song_url, headers=headers)
            song_soup = BeautifulSoup(song_data.text, 'html.parser')
            song_result = song_soup.select_one('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)').text
            melon_date = song_soup.select_one('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)')
            melon_date = melon_date.text.replace('.', '')

            # genre{0:락/메탈, 1:발라드, 2:인디/어쿠스틱, 3:트로트, 4: 힙합/R&B 5:댄스/POP/일렉트로닉스 6:기타 7:음악찾기실패 8:에러}
            if abs(int(melon_date) - int(spotify_date)) < 5:
                return selectGenre(song_result)
        except:
            print("no song2")
            break

    search_url = f"https://www.melon.com/search/total/index.htm?q={words}&section=&mwkLogType=T"
    search_data = requests.get(search_url, headers=headers)
    search_soup = BeautifulSoup(search_data.text, 'html.parser')
    for i in range(1, 11):
        try:
            search_result = search_soup.select_one(
                f'#frm_searchArtist > div > table > tbody > tr:nth-child({i}) > td:nth-child(1) > div > input')
            song_url = f"https://www.melon.com/song/detail.htm?songId={search_result['value']}"
            song_data = requests.get(song_url, headers=headers)
            song_soup = BeautifulSoup(song_data.text, 'html.parser')
            song_result = song_soup.select_one('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)').text
            melon_date = song_soup.select_one('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)')
            melon_date = melon_date.text.replace('.', '')

            if abs(int(melon_date) - int(spotify_date)) < 5:
                return selectGenre(song_result)
        except:
            print("no artist")
            return 9
    return 8

@csrf_exempt
def getCstInfo(request):
    received = json.loads(request.body)
    if request.method == 'POST':
        # allDB = serializers.serialize("json", Selected.objects.all())
        # allDB = json.loads(allDB)
        songData = {}
        # songData['name'] = "카세티 " + str(len(allDB) + 2) + "호"
        songData['name'] = received['name']
        songData['song1'] = received['song1_id']
        songData['song2'] = received['song2_id']
        songData['song3'] = received['song3_id']
        songData['song4'] = received['song4_id']
        songData['song5'] = received['song5_id']
        songData['text'] = received['text']

        data = {}
        # data['name'] = received['name']
        data['name'] = songData['name']
        data['energy'] = getEnergy(received['song1_id'])
        data['emotion'] = getEmotion(received['song2_id'])

        cid = 'cd36e22dd7b74a6083da70216f22a5dc'
        secret = 'a013e69375a84d9bbb387b941aec418d'
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        songData['songName'] = sp.track(track_id=received['song5_id'])['name']

        # temp = getGenre(received['song3_id'], received['song3_search'])
        # feature = sp.audio_features(tracks=[received['song3_id']])[0]["valence"]
        # if temp == 6 or temp == 7 or temp == 8:
        #     data['genre1'] = 5
        # else:
        #     data['genre1'] = temp

        data['genre1'] = getGenre(received['song3_id'], received['song3_search'])
        data['genre2'] = getGenre(received['song4_id'], received['song4_search'])
        data['songName'] = songData['songName']
        data['text'] = songData['text']

        songData['cst'] = str(data['energy']) + str(data['emotion']) + str(data['genre1']) + str(data['genre2'])

        print(data)
        songSerializer = SelectedSerializer(data=songData)
        if songSerializer.is_valid():
            songSerializer.save()

    return JsonResponse({'cassetti_info': data}, status=200)

