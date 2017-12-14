from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from api.views import ChannelViewSet, CategoryViewSet, SearchViewSet


router = routers.DefaultRouter()
router.register(r'channels', ChannelViewSet, 'channel')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'search', SearchViewSet, 'search')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='Sellers Channels API'), name='api-docs'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
