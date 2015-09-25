import six

if six.PY2:
    import basestring
elif six.PY3:
    basestring = (str, bytes)

if six.PY2:
    import urlparse
elif six.PY3:
    import urllib.parse as urlparse
