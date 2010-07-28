import os
import socket

from django.core.management.base import NoArgsCommand

from aggregator.models import Feed

LOCKFILE = "/tmp/update_feeds.lock"


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        socket.setdefaulttimeout(15)
        try:
            lockfile = os.open(LOCKFILE, os.O_CREAT | os.O_EXCL)
        except OSError:
            return
        try:
            self.update_feeds()

        finally:
            os.close(lockfile)
            os.unlink(LOCKFILE)

    def update_feeds(self):
        for feed in Feed.objects.filter(is_defunct=False):
            feed.update()
