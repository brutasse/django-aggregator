Django-aggregator
=================

A planet app for your Django project. It crawls a set of feeds, aggregates
them on a single page and re-publishes the entries with RSS and Atom feeds.

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
