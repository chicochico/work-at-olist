from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from api.views import ChannelViewSet, CategoryViewSet, SearchViewSet


schema_view = get_swagger_view(title='Channels API')
router = routers.DefaultRouter()
router.register(r'channels', ChannelViewSet, 'channel')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'search', SearchViewSet, 'search')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', schema_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
