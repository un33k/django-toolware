from django.conf import settings

TOOLWARE_DEBUG = getattr(settings, 'DEBUG', False)

LOGIN_URL = getattr(settings, 'LOGIN_URL', '/')
LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
