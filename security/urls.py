from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

def is_url_secure(url):
    return url_has_allowed_host_and_scheme(
        url, None, require_https=not settings.DEBUG)