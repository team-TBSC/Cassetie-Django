from rest_framework import serializers
from .models import Selected, Features

# # Serializers define the API representation.
# class SelectedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Selected
#         field = ['id', 'name', 'song1', 'song2', 'song3', 'song4', 'song5']
#
# class FeaturesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Features
#         field = ['id', 'name', 'energy', 'emotion', 'genre1', 'genre2', 'genre3']