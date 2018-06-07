from django.conf import settings
from django.core.mail import EmailMultiAlternatives

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')


def prepare_email_subject(content):
    """ Email subject must be text and a single line """
    subject = ''.join(content.splitlines())
    return subject


def send_multi_alt_email(
    subject_line,
    body_text,
    to_emails,
    body_html=None,
    from_email=DEFAULT_FROM_EMAIL,
    fail_silently=True
    ):
    """ Send a message to one more email address(s) """
    messenger = EmailMultiAlternatives(subject_line, body_text, from_email, to_emails)
    if body_html:
        messenger.attach_alternative(body_html, "text/html")
    try:
        messenger.send()
    except Exception as e:
        if not fail_silently:
            raise
