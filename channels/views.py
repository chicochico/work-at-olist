from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from .models import Channel
from .serializers import ListChannelSerializer, ChannelSerializer, CategorySerializer


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


class CategoryViewSet(viewsets.ViewSet):
    """Endpoints to access category by their identification."""

    def retrieve(self, request, pk=None):
        """Get a instance of category."""
        queryset = Channel.objects.exclude(parent=None)
        channel = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(channel, context={'request': request})
        return Response(serializer.data)


class SearchViewSet(viewsets.ViewSet):
    """Privide search functionality for channels and categories."""

    @list_route(methods=['get'], url_path='category/(?P<category_name>.+)')
    def search_category(self, request, category_name=None):
        """Search for categories that contains the search query."""
        queryset = Channel.objects.exclude(parent=None)
        queryset = get_list_or_404(queryset, name__icontains=category_name)
        serializer = CategorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='channel/(?P<channel_name>.+)')
    def search_channel(self, request, channel_name=None):
        """Search for channels that contains the search query."""
        queryset = Channel.objects.filter(parent=None)
        queryset = get_list_or_404(queryset, name__icontains=channel_name)
        serializer = ListChannelSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)