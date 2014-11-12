from django.conf.urls import patterns, include, url
from django.conf import settings  # For debugging.
from django.contrib import admin

from foia_hub.views import (
    contact_landing, learn,
    request_start, request_form, request_success)
from foia_hub.api import AgencyResource, OfficeResource,\
    FOIARequestResource, StatsResource


# Front-end
urlpatterns = patterns(
    '',
    url(r'^$', request_start, name='request'),
    url(r'^learn/?$', learn, name='learn'),
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
    url(r'^api/request/', include(FOIARequestResource.urls())),
    url(r'^api/stats/', include(StatsResource.urls())),

)

# Admin
admin.autodiscover()
urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

# For development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
