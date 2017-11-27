from django.contrib import admin
from channels.models import Channel
from mptt.admin import MPTTModelAdmin


class ChannelAdmin(MPTTModelAdmin):
    search_fields = ['name']
    readonly_fields = ('path',)

admin.site.register(Channel, ChannelAdmin)
