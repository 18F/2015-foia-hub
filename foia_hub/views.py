from django.http import HttpResponse
import datetime

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('foia_hub', 'templates'))

def request_form(request, slug=None):
    template = env.get_template('request/form.html')
    return HttpResponse(template.render(slug=slug))
