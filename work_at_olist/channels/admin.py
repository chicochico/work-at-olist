from django.contrib import admin
from .models import Channel
from mptt.admin import MPTTModelAdmin


admin.site.register(Channel, MPTTModelAdmin)
