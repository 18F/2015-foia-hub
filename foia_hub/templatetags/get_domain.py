from django_jinja import library
from urllib.parse import urlparse

@library.global_function
def get_domain(url):
    return "%s/..." % urlparse(url).netloc
