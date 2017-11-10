"""work_at_olist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from channels import views


router = routers.DefaultRouter()
router.register(r'channels', views.ChannelViewSet, 'channel')
router.register(r'categories', views.CategoryViewSet, 'category')
router.register(r'search', views.SearchViewSet, 'search')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/docs/', include_docs_urls(title='Sellers Channels API'), name='api-docs'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', RedirectView.as_view(url='/api/v1/docs', permanent=False), name='redirect-docs'),
]
