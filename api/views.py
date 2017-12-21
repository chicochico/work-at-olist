from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.response import Response
from channels.models import Channel, Category
from api.serializers import (CategorySerializer,
                             CategoryListSerializer,
                             ChannelSerializer,
                             ChannelListSerializer)


class ChannelViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """API endpoints for Channels, list, detail and search."""
    queryset = Channel.objects.all()
    lookup_field = 'name'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_serializer_class(self):
        """Use different serializer for lists and detail"""
        if self.action == 'list':
            return ChannelListSerializer
        elif self.action == 'retrieve':
            return ChannelSerializer
        return ChannelSerializer

    def retrieve(self, request, name=None):
        """Get a Channel detail with case insensitive name."""
        channel = get_object_or_404(self.queryset, name__iexact=name)
        serializer = ChannelSerializer(channel, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints for Categories, list, detail and search"""
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return CategorySerializer
        return CategorySerializer
