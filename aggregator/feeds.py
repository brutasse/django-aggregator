from django.contrib.syndication.views import Feed as BaseFeed

from aggregator.models import Entry


class Feed(BaseFeed):

    def items(self):
        return Entry.objects.select_related()[:10]

    def item_title(self, item):
        return '%s: %s' % (item.feed.title, item.title)

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return item.link

    def item_guid(self, item):
        return item.guid

    def item_pubdate(self, item):
        return item.date
