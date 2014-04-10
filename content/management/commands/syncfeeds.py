from datetime import datetime
from optparse import make_option
from time import mktime
from django.core.management import BaseCommand
import feedparser
from content.models import Feed, FeedEntry


class Command(BaseCommand):
    args = ''
    help = 'Synchronizes all feeds.'

    option_list = BaseCommand.option_list + (
        make_option('--feed',
                    action='store',
                    dest='feed',
                    default=None,
                    type='int',
                    help=''),
    )

    def handle(self, *args, **options):

        all_feeds = Feed.objects.all()
        for feed in all_feeds:
            self._import_feed(feed)

    @staticmethod
    def _import_feed(feed):
        fp = feedparser.parse(feed.url)
        print fp.feed
        feed.title = fp.feed.title
        #feed.description = fp.feed.description
        #feed.published = fp.feed.published_parsed
        feed.save()

        for entry in fp.entries:
            feedentry, foo = FeedEntry.objects.get_or_create(feed=feed, guid=entry.id)
            feedentry.title = entry.title
            feedentry.link = entry.link
            feedentry.description = entry.description
            feedentry.published = datetime.fromtimestamp(mktime(entry.published_parsed))

            feedentry.save()
