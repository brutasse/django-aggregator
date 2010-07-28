Django-aggregator
=================

A planet app for your Django project. It crawls a set of feeds, aggregates
them on a single page and re-publishes the entries with RSS and Atom feeds.

This app is based on `Django's community aggregator`_, updated to Django 1.2
and slightly improved.

.. _Django's community aggregator: http://www.djangoproject.com/community/

Installation
------------

::

    pip install -e git+git://github.com/brutasse/django-aggregator#egg=aggregator

**Requirements**:

* Django >= 1.2
* The universal feedparser

Configuration
-------------

Add ``aggregator`` to your ``INSTALLED_APPS`` & run ``syncdb``.

Templates
`````````

Create a simple view that renders a template. Use the following template tags
to fetch & render the data:

* ``{% load aggregator_tags %}`` to load the template library

* ``{% get_feed_list as feed_list %}`` to fetch the feeds

* ``{% get_entries <num_latest> as entries_list %}`` to fetch the latest
  entries

And then, to display the list of indexed feeds::

    <h2>Indexed feeds</h2>
    <ul>
        {% for feed in feed_list %}
            <li>{{ feed.title }} (<a href="{{ feed.public_url }}">site</a>)</li>
        {% endfor %}
    </ul>

To render the latest entries::

    <h2>Latest entries</h2>
    {% for entry in entries_list %}
        <div class="entry">
            <h2>{{ entry.feed.title }}: {{ entry.title|safe }}</h2>
            <p>{{ entry.summary|safe }}</p>
            <p>
                Published: {{ entry.date|date }}.
                <a href="{{ entry.link }}">Read more</a>
            </p>
        </div>
    {% endfor %}

If you want to render only a preview of the entries, you can do::

    {{ entry.summary|safe|truncatewords_html:30 }}

Feeds
`````

To publish some feeds of the aggregated content, subclass the base ``Feed``
class::

    from aggregator.feeds import Feed

    class MyAwesomeFeed(Feed):
        title = 'Aggregated content on <topic>'
        link = 'http://example.com'
        description = 'A more detailed description'

You can have Atom feeds::

    from django.utils.feedgenerator import Atom1Feed

    class MyAwesomeAtomFeed(MyAwesomeFeed):
        feed_type = Atom1Feed
        subtitle = MyAwesomeFeed.description

And add them to your URLs::

    from myproject.feeds import MyAwesomeFeed, MyAwesomeAtomFeed

    urlpatterns = patterns('',
        # ...
        url(r'^path/to/feeds/rss/$', MyAwesomeFeed(), name='aggregator_rss'),
        url(r'^path/to/feeds/atom/$', MyAwesomeAtomFeed(), name='aggregator_atom'),
        # ...
    )

When you're done you can add your feeds' URLs in the ``<head>`` section of
your website.

Usage
-----

Adding some feeds
`````````````````

Go to the admin and add the different feeds' name, title & URLs.

Updating the feeds
``````````````````

There are two management commands:

* ``mark_defunct_feeds`` will fetch all the registered feeds and check if they
  return a 404 or 500 response. If so, they are marked as "defunct" and will
  be skipped at each update.

* ``update_feeds`` fetches all the non-defunct feeds and checks for new
  content.

Here is how you could configure cron to schedule these two tasks::

    PYTHONPATH=/path/to/project
    DJANGO_SETTINGS_MODULE=settings_module

    15,45 * * * * python /path/to/manage.py update_feeds
    0 */6 * * *   python /path/to/manage.py mark_defunct_feeds
