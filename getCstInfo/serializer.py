from rest_framework import serializers
from .models import Selected
# from .models import Features

# Serializers define the API representation.
class SelectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selected
        fields = ['id', 'name', 'songName', 'cst', 'song1', 'song2', 'song3', 'song4', 'song5', 'text']


# class FeaturesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Features
#         fields = ['id', 'name', 'energy', 'emotion', 'genre1', 'genre2', 'genre3']