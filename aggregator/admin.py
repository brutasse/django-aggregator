from django.contrib import admin

from aggregator.models import Feed, Entry


class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'public_url', 'is_defunct')
    list_filter = ('is_defunct',)
    search_fields = ('title', 'public_url')
    list_per_page = 500


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'feed', 'date')
    list_filter = ('feed',)
    search_fields = ('feed__title', 'feed__public_url', 'title')
    date_hierarchy = 'date'

admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
