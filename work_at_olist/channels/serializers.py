from .models import Channel
from rest_framework import serializers


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.SerializerMethodField()
    categories_count = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('url', 'name', 'categories', 'categories_count')
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

    def get_categories(self, obj):
        return obj.get_all_categories()

    def get_categories_count(self, obj):
        return obj.get_categories_count()


class ListChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ('url', 'name')
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }
