__author__ = 'Val Neekman [neekware.com]'
__description__ = 'This application handles all common tasks. (hint: DRY)'
__version__ = '0.0.4'

from . import defaults

if defaults.TOOLWARE_TEMPLATE_TAGS_AUTO_LOAD:
    from django import template
    try:
        add_to_builtins = template.add_to_builtins
    except AttributeError:
        add_to_builtins = template.base.add_to_builtins
    application_tags = [
        'toolware.templatetags.forms',
        'toolware.templatetags.rounder',
        'toolware.templatetags.highlight',
        'toolware.templatetags.variable',
        'toolware.templatetags.strings',
        'toolware.templatetags.klass',
        'toolware.templatetags.email',
        'toolware.templatetags.generic',
    ]
    for t in application_tags: add_to_builtins(t)

