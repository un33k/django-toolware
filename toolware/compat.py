import six

if six.PY2:
    basestring = basestring
elif six.PY3:
    basestring = (str, bytes)

if six.PY2:
    import urlparse
elif six.PY3:
    import urllib.parse as urlparse

try:
    from .urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

try:
    import HTMLParser

    def unescape(html):
        return HTMLParser.HTMLParser().unescape(html)
except ImportError:
    from html import unescape

if six.PY2:
    from urllib import quote
elif six.PY3:
    from urllib.parse import quote
