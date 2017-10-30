from django.contrib import admin
from .models import Category, Channel


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass
