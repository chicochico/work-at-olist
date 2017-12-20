from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from channels.models import Channel, Category
from api.serializers import (CategorySerializer,
                             CategoryListSerializer,
                             ChannelSerializer,
                             ChannelListSerializer)


class ChannelViewSet(viewsets.ViewSet):
    """API endpoints for Channels"""
    lookup_field = 'name'

    def get_queryset(self):
        return Channel.objects.all()

    def list(self, request):
        serializer = ChannelListSerializer(self.get_queryset(),
                                           many=True,
                                           context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, name=None):
        channel = get_object_or_404(self.get_queryset(), name=name)
        serializer = ChannelSerializer(channel, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ViewSet):
    """API endpoints for Categories"""
    def get_queryset(self):
        return Category.objects.all()

    def list(self, request):
        serializer = CategoryListSerializer(self.get_queryset(),
                                            many=True,
                                            context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)


