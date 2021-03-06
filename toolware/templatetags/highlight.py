import re
from django import template
from django.template import Node, TemplateSyntaxError
from django.conf import settings
from django.utils.safestring import mark_safe
from ..utils.query import get_text_tokenizer

register = template.Library()


def highlight_text(needles, haystack, cls_name='highlighted', words=False, case=False):
    """ Applies cls_name to all needles found in haystack. """

    if not needles:
        return haystack
    if not haystack:
        return ''

    if words:
        pattern = r"(%s)" % "|".join(['\\b{}\\b'.format(re.escape(n)) for n in needles])
    else:
        pattern = r"(%s)" % "|".join([re.escape(n) for n in needles])

    if case:
        regex = re.compile(pattern)
    else:
        regex = re.compile(pattern, re.I)

    i, out = 0, ""
    for m in regex.finditer(haystack):
        out += "".join([haystack[i:m.start()], '<span class="%s">' % cls_name,
            haystack[m.start():m.end()], "</span>"])
        i = m.end()
    return mark_safe(out + haystack[i:])


@register.filter
def highlight(string, keywords, cls_name='highlighted'):
    """ Given an list of words, this function highlights the matched text in the given string. """

    if not keywords:
        return string
    if not string:
        return ''
    include, exclude = get_text_tokenizer(keywords)
    highlighted = highlight_text(include, string, cls_name)
    return highlighted


@register.filter
def highlight_words(string, keywords, cls_name='highlighted'):
    """ Given an list of words, this function highlights the matched words in the given string. """

    if not keywords:
        return string
    if not string:
        return ''
    include, exclude = get_text_tokenizer(keywords)
    highlighted = highlight_text(include, string, cls_name, words=True)
    return highlighted
