from django.contrib import admin
from .models import CategoryTree, Channel
from mptt.admin import MPTTModelAdmin


admin.site.register(CategoryTree, MPTTModelAdmin)
admin.site.register(Channel)
