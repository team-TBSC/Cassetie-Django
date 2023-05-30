import json
from getCstInfo.models import Selected
from django.http import JsonResponse
from django.core import serializers
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def getDB(request):
    if request.method == 'GET':
        allDB = serializers.serialize("json", Selected.objects.all())
        allDB = json.loads(allDB)

        cid = 'cd36e22dd7b74a6083da70216f22a5dc'
        secret = 'a013e69375a84d9bbb387b941aec418d'
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        data = []

        start = 0
        if len(allDB) > 15:
            start = len(allDB) - 15
        for i in range(start, len(allDB)):

            data_temp = {}
            data_temp['name'] = allDB[i]['fields']['name']
            data_temp['num'] = allDB[i]['fields']['cst']
            data_temp['text'] = allDB[i]['fields']['text']
            data_temp['song'] = []

            info = sp.track(track_id=allDB[i]['fields']['song1'])
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            # temp['preview_url'] = info['preview_url']
            # data_temp['song1'] = temp
            data_temp['song'].append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song2'])
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            # temp['preview_url'] = info['preview_url']
            # data_temp['song2'] = temp
            data_temp['song'].append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song3'])
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            # temp['preview_url'] = info['preview_url']
            # data_temp['song3'] = temp
            data_temp['song'].append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song4'])
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            # temp['preview_url'] = info['preview_url']
            # data_temp['song4'] = temp
            data_temp['song'].append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song5'])
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            # temp['preview_url'] = info['preview_url']
            # data_temp['song5'] = temp
            data_temp['song'].append(temp)

            data.append(data_temp)

        print(data)

    return JsonResponse({'db_data': data}, status=200)

def getLastDB(request):
    if request.method == 'GET':
        allDB = serializers.serialize("json", Selected.objects.all())
        allDB = json.loads(allDB)
        data = {}
        data['name'] = allDB[len(allDB)-1]['fields']['name']
        data['result'] = allDB[len(allDB)-1]['fields']['cst']
        data['songName'] = allDB[len(allDB) - 1]['fields']['songName']
        data['text'] = allDB[len(allDB) - 1]['fields']['text']

        return JsonResponse(data=data, status=200)


