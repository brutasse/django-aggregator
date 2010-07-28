"""
Mark people with 404'ing feeds as defunct.
"""
import urllib2

from django.core.management.base import NoArgsCommand

from aggregator.models import Feed


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        for feed in Feed.objects.all():
            try:
                response = urllib2.urlopen(feed.feed_url)
            except urllib2.HTTPError, e:
                if e.code == 404 or e.code == 500:
                    print "%s on %s; marking defunct" % (e.code, feed)
                    feed.is_defunct = True
                    feed.save()
                else:
                    raise
