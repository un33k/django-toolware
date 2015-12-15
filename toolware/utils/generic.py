import re
import uuid
import six
import datetime
import hashlib
import urllib
from django.utils.encoding import smart_str
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone

from ..compat import urlparse
from ..compat import parse_qs

simple_email_re = re.compile(r'^\S+@\S+\.\S+$')


def get_uuid(length=32, version=1):
    """
    Returns a unique ID of a given length.
    User `version=2` for cross-systems uniqueness.
    """
    if version == 1:
        return uuid.uuid1().hex[:length]
    else:
        return uuid.uuid4().hex[:length]


def get_integer(value='0'):
    """
    Converts string to integer.
    If string has non-numerical character, it returns None
    """
    try:
        return int(value)
    except ValueError:
        return None


def get_hashed(key):
    """
    Returns a hashed version of a given key.
    One way encryption.
    """
    return hashlib.md5(key.encode('utf-8')).hexdigest()


def get_days_ago(days=0):
    """
    Return X 'days' ago in datetime format
    """
    return (timezone.now() - datetime.timedelta(days))


def get_days_from_now(days=0):
    """
    Return X 'days' from today in datetime format
    """
    return (timezone.now() + datetime.timedelta(days))


def get_dict_to_encoded_url(data):
    """
    Converts a dict to an encoded URL.
    Example: given  data = {'a': 1, 'b': 2}, it returns 'a=1&b=2'
    """
    unicode_data = dict([(k, smart_str(v)) for k, v in data.items()])
    encoded = urllib.urlencode(unicode_data)
    return encoded


def get_encoded_url_to_dict(string):
    """
    Converts an encoded URL to a dict.
    Example: given string = 'a=1&b=2' it returns {'a': 1, 'b': 2}
    """
    data = urlparse.parse_qsl(string, keep_blank_values=True)
    data = dict(data)
    return data


def remove_csrf_from_params_dict(data):
    """
    Removes csrf token from a dict
    """
    pd = data
    try:
        del pd['csrfmiddlewaretoken']
    except KeyError:
        pass
    return pd


def get_unique_key_from_get(get_dict):
    """
    Build a unique key from get data
    """
    site = Site.objects.get_current()
    key = get_dict_to_encoded_url(get_dict)
    cache_key = '{}_{}'.format(site.domain, key)
    return hashlib.md5(cache_key).hexdigest()


def get_unique_key_from_post(post_dict):
    """
    Build a unique key from post data
    """
    post_dict = remove_csrf_from_params_dict(post_dict)
    return get_unique_key_from_get(post_dict)


def tobin(deci_num, len=32):
    """
    Given a decimal number, returns a string bitfield of length = len
    Example: given deci_num = 1 and len = 10, it return 0000000001
    """
    bitstr = "".join(map(lambda y: str((deci_num >> y) & 1), range(len - 1, -1, -1)))
    return bitstr


def is_valid_email(email):
    """
    Validates and email address.
    Note: valid emails must follow the <name>@<domain><.extension> patterns.
    """
    try:
        validate_email(email)
    except ValidationError:
        return False
    if simple_email_re.match(email):
        return True
    return False


def get_domain(url):
    if 'http' not in url.lower():
        url = 'http://{}'.format(url)
    return urlparse(url).hostname


def get_url_args(url):
    url_data = urlparse.urlparse(url)
    arg_dict = parse_qs(url_data.query)
    return arg_dict
