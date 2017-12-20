from django.urls import reverse
from channels.models import Channel, Category
from rest_framework import serializers


class ChannelListSerializer(serializers.ModelSerializer):
    """Serializer for lists of channels"""
    class Meta:
        model = Channel
        fields = (
            'url',
            'name',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class CategoryListSerializer(serializers.ModelSerializer):
    """Serializer for lists of categories"""
    channel = serializers.HyperlinkedRelatedField(many=False,
                                                  lookup_field='name',
                                                  view_name='channel-detail',
                                                  read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'path', 'channel')


class SubcategoryListSerializer(serializers.ModelSerializer):
    """Serializer for lists of subcategories"""
    class Meta:
        model = Category
        fields = ('url', 'name', 'path')


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for channel detail"""
    subcategories = SubcategoryListSerializer(many=True)

    class Meta:
        model = Channel
        fields = (
            'url',
            'name',
            'subcategories_count',
            'subcategories',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category detail"""
    channel = serializers.HyperlinkedRelatedField(view_name='channel-detail',
                                                  lookup_field='name',
                                                  many=False,
                                                  read_only=True)
    parent = serializers.SerializerMethodField()
    subcategories = SubcategoryListSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'url',
            'name',
            'path',
            'channel',
            'parent',
            'subcategories_count',
            'subcategories',
        )

    def get_parent(self, obj):
        if obj.level == 1:
            return None
        else:
            url = reverse('category-detail', args=[obj.parent.pk])
            return self.context['request'].build_absolute_uri(url)
