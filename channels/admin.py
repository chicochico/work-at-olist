from django.contrib import admin
from channels.models import Channel
from mptt.admin import MPTTModelAdmin


admin.site.register(Channel, MPTTModelAdmin)
