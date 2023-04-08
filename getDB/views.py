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
        #
        for i in range(len(allDB)):
            data_temp = []
            data_temp.append(allDB[i]['fields']['name'])
            data_temp.append(allDB[i]['fields']['cst'])

            info = sp.track(track_id=allDB[i]['fields']['song1'], market='KR')
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            temp['preview_url'] = info['preview_url']
            data_temp.append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song2'], market='KR')
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            temp['preview_url'] = info['preview_url']
            data_temp.append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song3'], market='KR')
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            temp['preview_url'] = info['preview_url']
            data_temp.append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song4'], market='KR')
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            temp['preview_url'] = info['preview_url']
            data_temp.append(temp)

            info = sp.track(track_id=allDB[i]['fields']['song5'], market='KR')
            temp = {}
            temp['track'] = info['name']
            temp['artist'] = info['artists'][0]['name']
            temp['image'] = info['album']['images'][0]['url']
            temp['preview_url'] = info['preview_url']
            data_temp.append(temp)

            data.append(data_temp)

        print(data)

    return JsonResponse({'db_data': data}, status=200)

def getLastDB(request):
    if request.method == 'GET':
        allDB = serializers.serialize("json", Selected.objects.all())
        allDB = json.loads(allDB)
        data = {}
        data['result'] = allDB[len(allDB)-1]['fields']['cst']

        return JsonResponse(data=data, status=200)


