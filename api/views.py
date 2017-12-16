from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from channels.models import Channel, Category
from api.serializers import ListChannelSerializer, ChannelSerializer, CategorySerializer


class ChannelViewSet(viewsets.ViewSet):
    """
    Endpoints to access channels.
    """
    lookup_field = 'name'

    def list(self, request):
        """
        List all avaliable channels and the url to access them.
        """
        queryset = Channel.objects.all()
        serializer = ListChannelSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, name=None):
        """
        Lookup a specific channel with its name.
        """
        queryset = Channel.objects.all()
        channel = get_object_or_404(queryset, name=name)
        serializer = ChannelSerializer(channel, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ViewSet):
    """
    Endpoints to access category by their identification.
    """

    def retrieve(self, request, pk=None):
        """
        Get a instance of category.
        """
        queryset = Category.objects.all()
        channel = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(channel, context={'request': request})
        return Response(serializer.data)


class SearchViewSet(viewsets.ViewSet):
    """
    Provide search functionality for channels and categories.
    """

    @list_route(methods=['get'], url_path='category/(?P<category_name>.+)', url_name='category')
    def search_category(self, request, category_name=None):
        """
        Search for categories that contains the search query.
        """
        queryset = Category.objects.all()
        queryset = get_list_or_404(queryset, name__icontains=category_name)
        serializer = CategorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='channel/(?P<channel_name>.+)', url_name='channel')
    def search_channel(self, request, channel_name=None):
        """
        Search for channels that contains the search query.
        """
        queryset = Channel.objects.all()
        queryset = get_list_or_404(queryset, name__icontains=channel_name)
        serializer = ListChannelSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
