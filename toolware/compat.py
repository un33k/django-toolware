import six

if six.PY2:
    import basestring
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
    unescape = HTMLParser.HTMLParser()
except ImportError:
    from html import unescape
