from channels.models import Channel
from rest_framework import serializers


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('url', 'name', 'categories', 'categories_count')
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

    def get_categories(self, obj):
        return obj.get_all_categories_paths()


class ListChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Channel
        fields = ('url', 'name')
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class CategorySerializer(serializers.Serializer):
    url = serializers.HyperlinkedRelatedField(
        source='pk',
        view_name='category-detail',
        many=False,
        read_only=True,
        lookup_field='pk',
    )
    name = serializers.CharField()
    path = serializers.CharField()
    subcategories = serializers.SerializerMethodField()
    channel = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='channel-detail',
        lookup_field='name',
    )

    def get_subcategories(self, obj):
        return obj.get_all_categories_paths()
