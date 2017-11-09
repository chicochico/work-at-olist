from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Channel
from .serializers import ListChannelSerializer, ChannelSerializer


class ChannelViewSet(viewsets.ViewSet):
    """Endpoints to access channels."""
    lookup_field = 'name'

    def list(self, request):
        """List all avaliable channels and the url to access them."""
        queryset = Channel.objects.filter(parent=None)
        serializer = ListChannelSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, name=None):
        """Lookup a specific channel thru its name."""
        queryset = Channel.objects.filter(parent=None)
        channel = get_object_or_404(queryset, name=name)
        serializer = ChannelSerializer(channel, context={'request': request})
        return Response(serializer.data)
