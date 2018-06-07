import html2text
import markdown


def md_to_html(content):
    """ Converts markdown content to HTML """
    html = markdown.markdown(content)
    return html


def md_to_text(content):
    """ Converts markdown content to text """
    text = None
    html = markdown.markdown(content)
    if html:
        text = html_to_text(content)
    return text


def md_to_plain(content):
    """ Converts markdown content to plain text """
    plain = None
    html = markdown.markdown(content)
    if html:
      h2t = html2text.HTML2Text()
      h2t.ignore_links = False
      plain = h2t.handle(html)
    return plain


def singleline_content(content):
    """ Converts multiline content to a single line """
    return ''.join(content.splitlines())


def parts_to_uri(base_uri, uri_parts):
    """
    Converts uri parts to valid uri.
    Example: /memebers, ['profile', 'view'] => /memembers/profile/view
    """
    uri = "/".join(map(lambda x: str(x).rstrip('/'), [base_uri] + uri_parts))
    return uri


def domain_to_fqdn(domain, proto=None):
    """ returns a fully qualified app domain name """
    from .generic import get_site_proto
    proto = proto or get_site_proto()
    fdqn = '{proto}://{domain}'.format(proto=proto, domain=domain)
    return fdqn