import re
import datetime
from django.db.models import Q
from django.db import models
from django.db.models.query import QuerySet

from .generic import get_integer, get_days_ago, get_days_from_now


class CaseInsensitiveQuerySet(QuerySet):
    """
    Custom QuerySet to treat queries on special field(s) as case insensitive.
    Models fields that should be treated as case-insensitive should be place in
    CASE_INSENSITIVE_FIELDS with in the model class.
    Example: CASE_INSENSITIVE_FIELDS = ['username', 'email',]
    """
    def case_insensitive(self, **fields_dict):
        """
        Converts queries to case insensitive for special fields.
        """
        if hasattr(self.model, 'CASE_INSENSITIVE_FIELDS'):
            for field in self.model.CASE_INSENSITIVE_FIELDS:
                if field in fields_dict:
                    fields_dict[field + '__iexact'] = fields_dict[field]
                    del fields_dict[field]

    def filter(self, *args, **kwargs):
        self.case_insensitive(**kwargs)
        return super(CaseInsensitiveQuerySet, self).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        self.case_insensitive(**kwargs)
        return super(CaseInsensitiveQuerySet, self).exclude(*args, **kwargs)

    def complex_filter(self, filter_obj):
        if isinstance(filter_obj, dict):
            self.case_insensitive(**filter_obj)
        return super(CaseInsensitiveQuerySet, self).complex_filter(filter_obj)


class CaseInsensitiveManager(models.Manager):
    """
    Custom Case Insensitive Manager Class.
    """
    def get_queryset(self):
        return CaseInsensitiveQuerySet(self.model)


class GetUniqueOrNoneManager(models.Manager):
    """
    Adds get_unique_or_none method to objects
    """
    def get_unique_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None


def get_text_tokenizer(query_string):
    """
    Tokenize the input string and return two lists, exclude list is for words that
    start with a dash (ex: -word) and include list is for all other words
    """
    # Regex to split on double-quotes, single-quotes, and continuous non-whitespace characters.
    split_pattern = re.compile('("[^"]+"|\'[^\']+\'|\S+)')

    # Pattern to remove more than one inter white-spaces and more than one "-"
    space_cleanup_pattern = re.compile('[\s]{2,}')
    dash_cleanup_pattern = re.compile('^[-]{2,}')

    # Return the list of keywords.
    keywords = [dash_cleanup_pattern.sub('-', space_cleanup_pattern.sub(' ', t.strip(' "\'')))
        for t in split_pattern.findall(query_string) if len(t.strip(' "\'')) > 0]
    include = [word for word in keywords if not word.startswith('-')]
    exclude = [word.lstrip('-') for word in keywords if word.startswith('-')]
    return include, exclude


def get_query_includes(tokenized_terms, search_fields):
    """
    Builds a query for included terms in a text search.
    """
    query = None
    for term in tokenized_terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def get_query_excludes(tokenized_terms, search_fields):
    """
    Builds a query for excluded terms in a text search.
    """
    query = None
    for term in tokenized_terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query


def get_text_query(query_string, search_fields):
    """
    Builds a query for both included & excluded terms in a text search.
    """
    include_terms, exclude_terms = get_text_tokenizer(query_string)
    include_q = get_query_includes(include_terms, search_fields)
    exclude_q = get_query_excludes(exclude_terms, search_fields)
    query = None
    if include_q and exclude_q:
        query = include_q & ~exclude_q
    elif not exclude_q:
        query = include_q
    else:
        query = ~exclude_q
    return query


def get_date_greater_query(days, date_field):
    """
    Query for if date_field is within number of "days" ago.
    """
    query = None
    days = get_integer(days)
    if days:
        past = get_days_ago(days)
        query = Q(**{"%s__gte" % date_field: past.isoformat()})
    return query


def get_date_less_query(days, date_field):
    """
    Query for if date_field is within number of "days" from now.
    """
    query = None
    days = get_integer(days)
    if days:
        future = get_days_from_now(days)
        query = Q(**{"%s__lte" % date_field: future.isoformat()})
    return query


def get_null_query(field=None):
    """
    Query for null field.
    """
    if not field:
        return field
    null_q = Q(**{"%s__isnull" % field: True})
    return null_q


def get_blank_query(field=None):
    """.
    Query for blank field.
    """
    if not field:
        return field
    blank_q = Q(**{field: ''})
    return blank_q


def get_null_or_blank_query(field=None):
    """
    Query for null or blank field.
    """
    if not field:
        return field
    null_q = get_null_query(field)
    blank_q = get_blank_query(field)
    return (null_q | blank_q)


def get_not_null_and_not_blank_query(field=None):
    """
    Query for not null and not blank fields.
    """
    return ~ get_null_or_blank_query(field)
