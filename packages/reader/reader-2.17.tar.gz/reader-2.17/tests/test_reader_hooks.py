from datetime import datetime

from fakeparser import FailingParser
from fakeparser import NotModifiedParser
from fakeparser import Parser

from reader import EntryUpdateStatus
from reader._types import EntryData


def test_after_entry_update_hooks(reader):
    reader._parser = parser = Parser()
    parser.tzinfo = False

    plugin_calls = []

    def first_plugin(r, e, s):
        assert r is reader
        plugin_calls.append((first_plugin, e, s))

    def second_plugin(r, e, s):
        assert r is reader
        plugin_calls.append((second_plugin, e, s))

    feed = parser.feed(1, datetime(2010, 1, 1))
    one = parser.entry(1, 1, datetime(2010, 1, 1))
    reader.add_feed(feed.url)
    reader.after_entry_update_hooks.append(first_plugin)
    reader.update_feeds()
    assert plugin_calls == [(first_plugin, one, EntryUpdateStatus.NEW)]
    assert set(e.id for e in reader.get_entries()) == {'1, 1'}

    plugin_calls[:] = []

    feed = parser.feed(1, datetime(2010, 1, 2))
    one = parser.entry(1, 1, datetime(2010, 1, 2))
    two = parser.entry(1, 2, datetime(2010, 1, 2))
    reader.after_entry_update_hooks.append(second_plugin)
    reader.update_feeds()
    assert plugin_calls == [
        (first_plugin, two, EntryUpdateStatus.NEW),
        (second_plugin, two, EntryUpdateStatus.NEW),
        (first_plugin, one, EntryUpdateStatus.MODIFIED),
        (second_plugin, one, EntryUpdateStatus.MODIFIED),
    ]
    assert set(e.id for e in reader.get_entries()) == {'1, 1', '1, 2'}

    # TODO: What is the expected behavior if a plugin raises an exception?


def test_after_entry_update_hooks_add_entry(reader):
    reader.add_feed('1')

    plugin_calls = []

    def first_plugin(r, e, s):
        assert r is reader
        plugin_calls.append((first_plugin, e, s))

    def second_plugin(r, e, s):
        assert r is reader
        plugin_calls.append((second_plugin, e, s))

    reader.after_entry_update_hooks.append(first_plugin)
    reader.after_entry_update_hooks.append(second_plugin)

    entry = EntryData('1', '1, 1', title='title')

    reader.add_entry(entry)

    assert plugin_calls == [
        (first_plugin, entry, EntryUpdateStatus.NEW),
        (second_plugin, entry, EntryUpdateStatus.NEW),
    ]


def test_feed_update_hooks(reader):
    reader._parser = parser = Parser()
    parser.tzinfo = False

    plugin_calls = []

    def before_plugin(r, f):
        assert r is reader
        plugin_calls.append((before_plugin, f))

    def first_plugin(r, f):
        assert r is reader
        plugin_calls.append((first_plugin, f))

    def second_plugin(r, f):
        assert r is reader
        plugin_calls.append((second_plugin, f))

    # TODO: these should all be different tests

    # base case
    one = parser.feed(1, datetime(2010, 1, 1))
    parser.entry(1, 1, datetime(2010, 1, 1))
    reader.add_feed(one)
    reader.after_feed_update_hooks.append(first_plugin)
    reader.before_feed_update_hooks.append(before_plugin)
    reader.update_feeds()
    assert plugin_calls == [(before_plugin, one.url), (first_plugin, one.url)]

    plugin_calls[:] = []

    # gets called if something changes
    parser.entry(1, 1, datetime(2010, 1, 2))
    reader.update_feeds()
    assert plugin_calls == [(before_plugin, one.url), (first_plugin, one.url)]

    plugin_calls[:] = []

    # gets called even if there was no change
    reader.update_feeds()
    assert plugin_calls == [(before_plugin, one.url), (first_plugin, one.url)]

    plugin_calls[:] = []

    # gets called even if the feed was not modified
    reader._parser = NotModifiedParser()
    reader.update_feeds()
    assert plugin_calls == [(before_plugin, one.url), (first_plugin, one.url)]

    plugin_calls[:] = []

    # gets called even if there was an error
    reader._parser = FailingParser()
    reader.update_feeds()
    assert plugin_calls == [(before_plugin, one.url), (first_plugin, one.url)]

    plugin_calls[:] = []

    # plugin order and feed order is maintained
    reader._parser = parser
    two = parser.feed(2, datetime(2010, 1, 1))
    reader.add_feed(two)
    reader.after_feed_update_hooks.append(second_plugin)
    reader.update_feeds()
    assert plugin_calls == [
        (before_plugin, one.url),
        (first_plugin, one.url),
        (second_plugin, one.url),
        (before_plugin, two.url),
        (first_plugin, two.url),
        (second_plugin, two.url),
    ]

    plugin_calls[:] = []

    # update_feed() only runs hooks for that plugin
    reader.update_feed(one)
    assert plugin_calls == [
        (before_plugin, one.url),
        (first_plugin, one.url),
        (second_plugin, one.url),
    ]

    # TODO: What is the expected behavior if a plugin raises an exception?


def test_feeds_update_hooks(reader):
    reader._parser = parser = Parser()
    parser.tzinfo = False

    plugin_calls = []

    def before_feed_plugin(r, f):
        assert r is reader
        plugin_calls.append((before_feed_plugin, f))

    def after_feed_plugin(r, f):
        assert r is reader
        plugin_calls.append((after_feed_plugin, f))

    def before_feeds_plugin(r):
        assert r is reader
        plugin_calls.append((before_feeds_plugin,))

    def after_feeds_plugin(r):
        assert r is reader
        plugin_calls.append((after_feeds_plugin,))

    reader.before_feed_update_hooks.append(before_feed_plugin)
    reader.after_feed_update_hooks.append(after_feed_plugin)
    reader.before_feeds_update_hooks.append(before_feeds_plugin)
    reader.after_feeds_update_hooks.append(after_feeds_plugin)

    # TODO: these should all be different tests

    # no feeds
    reader.update_feeds()
    assert plugin_calls == [(before_feeds_plugin,), (after_feeds_plugin,)]

    plugin_calls[:] = []

    # two feeds + feed vs feeds order
    one = parser.feed(1, datetime(2010, 1, 1))
    two = parser.feed(2, datetime(2010, 1, 1))
    reader.add_feed(one)
    reader.add_feed(two)
    reader.update_feeds()
    assert plugin_calls[0] == (before_feeds_plugin,)
    assert plugin_calls[-1] == (after_feeds_plugin,)
    assert set(plugin_calls[1:-1]) == {
        (before_feed_plugin, one.url),
        (after_feed_plugin, one.url),
        (before_feed_plugin, two.url),
        (after_feed_plugin, two.url),
    }

    plugin_calls[:] = []

    # not called for update_feed()
    reader.update_feed(one)
    assert set(plugin_calls) == {
        (before_feed_plugin, one.url),
        (after_feed_plugin, one.url),
    }

    plugin_calls[:] = []

    # called even if there's an error
    reader._parser = FailingParser()
    reader.update_feeds()
    assert plugin_calls[0] == (before_feeds_plugin,)
    assert plugin_calls[-1] == (after_feeds_plugin,)
    assert set(plugin_calls[1:-1]) == {
        (before_feed_plugin, one.url),
        (after_feed_plugin, one.url),
        (before_feed_plugin, two.url),
        (after_feed_plugin, two.url),
    }


# TODO: test relative order of different hooks
