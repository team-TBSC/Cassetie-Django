"""cassetti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from getMusicList import views as getMusicListViews
from getCstInfo import views as getCstInfoViews

from django.urls import path, include
from django.contrib.auth.models import User
from getCstInfo.models import Selected, Features
# from getCstInfo.serializer import SelectedSerializer, FeaturesSerializer
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class SelectedViewSet(viewsets.ModelViewSet):
#     queryset = Selected.objects.all()
#     serializer_class = SelectedSerializer
#
# class FeaturesViewSet(viewsets.ModelViewSet):
#     queryset = Features.objects.all()
#     serializer_class = FeaturesSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'getMusicList', SelectedViewSet)
# router.register(r'getCstInfo', FeaturesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('getMusicList/', getMusicListViews.getMusicList),
    path('getCstInfo/', getCstInfoViews.getCstInfo),
]
