from django.template import Context, Template


def render_template(content, context):
    """ renders context aware template """
    rendered = Template(content).render(Context(context))
    return rendered
