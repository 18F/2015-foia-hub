from django.conf.urls import patterns, include, url
from django.conf import settings  # For debugging.
from django.contrib import admin
from django.views.generic import TemplateView

from foia_hub.views import (
    contact_landing,
    request_start, request_autocomplete, request_form, request_success)
from foia_hub.api import AgencyResource, OfficeResource, FOIARequestResource
from foia_hub.api import AgencyOfficeResource


# Front-end
urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(
        r'^learn/?$',
        TemplateView.as_view(template_name="learn.html"), name='learn'),

    url(r'^contacts/(?P<slug>[-\w]+)/?$', contact_landing,
        name='contact_landing'),
    url(r'^request/?$', request_start, name='request'),
    url(r'^request/autocomplete?$', request_autocomplete, name='autocomplete'),
    url(r'^request/(?P<slug>[-\w]+)/$', request_form, name='form'),
    url(r'^request/success/(?P<id>[\d]+)/$', request_success, name='success')
)

# APIs
urlpatterns += patterns(
    '',
    url(r'^api/agency/(?P<slug>[-\w]+)/$', include(OfficeResource.urls())),
    url(r'^api/agency/', include(AgencyResource.urls())),
    url(r'^api/agencyoffice/', include(AgencyOfficeResource.urls())),
    url(r'^api/request/', include(FOIARequestResource.urls())),
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
