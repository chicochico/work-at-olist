from django.contrib import admin
from channels.models import Channel, Category
from mptt.admin import MPTTModelAdmin


class ChannelAdmin(MPTTModelAdmin):
    fields = ('name',)
    search_fields = ['name']

class CategoryAdmin(MPTTModelAdmin):
    search_fields = ['name']
    readonly_fields = ('path',)


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Category, CategoryAdmin)
