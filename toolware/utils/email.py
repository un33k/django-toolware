from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage


DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')


def prepare_email_subject(content):
    """ Email subject must be text and a single line """
    subject = ''.join(content.splitlines())
    return subject


def send_multi_alt_email(
    subject,  # single line with no line-breaks
    text_content,
    to_emails,
    html_content=None,
    from_email=DEFAULT_FROM_EMAIL,
    fail_silently=True
    ):
    """ 
    Send a message to one more email address(s).
    With text content as primary and html content as alternative.
    """
    messenger = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    if html_content:
        messenger.attach_alternative(html_content, "text/html")
    try:
        messenger.send()
    except Exception as e:
        if not fail_silently:
            raise


def send_html_email(
    subject,  # single line with no line-breaks
    html_content,
    to_emails,
    from_email=DEFAULT_FROM_EMAIL,
    fail_silently=True
    ):
    """ 
    Send a message to one more email address(s).
    With html content as primary.
    """
    messenger = EmailMessage(subject, html_content, from_email, to_emails)
    messenger.content_subtype = "html"  # Main content is now text/html
    try:
        messenger.send()
    except Exception as e:
        if not fail_silently:
            raise
