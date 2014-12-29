from django.conf.urls import patterns, include, url
from django.conf import settings  # For debugging.
from django.contrib import admin

from foia_hub.views import (
    contact_landing, learn, about, agencies, developers,
    home, request_form, request_success)

from foia_hub.api import AgencyResource, OfficeResource, FOIARequestResource


# Front-end
urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^learn/?$', learn, name='learn'),
    url(r'^about/?$', about, name='about'),
    url(r'^agencies/?$', agencies, name='agencies'),
    url(r'^developers/?$', developers, name='developers'),
    url(r'^contacts/(?P<slug>[-\w]+)/?$', contact_landing,
        name='contact_landing'),
    url(r'^request/(?P<slug>[-\w]+)/$', request_form, name='form'),
    url(r'^request/success/(?P<id>[\d]+)/$', request_success, name='success')
)

# APIs
urlpatterns += patterns(
    '',
    url(r'^api/agency/', include(AgencyResource.urls())),
    url(r'^api/office/', include(OfficeResource.urls())),
)

if settings.SHOW_WEBFORM:
    urlpatterns += patterns(
        '',
        url(r'^api/request/', include(FOIARequestResource.urls())))

# Admin
admin.autodiscover()
urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

# For development
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += patterns(
            '',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
    except ImportError:
        pass
