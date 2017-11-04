from django.contrib import admin
from .models import Category, Channel
from mptt.admin import MPTTModelAdmin


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Channel)
