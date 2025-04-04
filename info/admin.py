from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'modified', 'is_active']
    list_filter = ['is_active', 'created']
    search_fields = ['title', 'content']
