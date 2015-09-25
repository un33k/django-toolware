from django import template

register = template.Library()


@register.assignment_tag()
def sizeof(collection):
    """
    Usage:
    {% sizeof mylist as mylistsize %}
    """

    size = len(collection)
    return size


@register.filter
def splitBy(data, num):
    """ Turn a list to list of list """
    return [data[i:i + num] for i in range(0, len(data), num)]
