from django.conf.urls import patterns, url
from contact_updater.views import prepopulate_agency, form_index

urlpatterns = patterns(
    '',
    url(r'^$', form_index, name='contact_updater_index'),
    url(r'^(?P<slug>[-\w]+)/?$',
        prepopulate_agency,
        name='contact_updater_form'),
)
