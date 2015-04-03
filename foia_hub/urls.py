from django.conf.urls import patterns, include, url
from django.conf import settings  # For debugging.
from django.contrib import admin
from django.views.generic import TemplateView

from foia_hub.views import (
    SmallSearchView, contact_landing, agencies,
    request_form, request_noop)

from foia_hub.api import AgencyResource, OfficeResource, FOIARequestResource

import contact_updater.urls as contact_updater_urls

# Front-end
urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^learn/?$', SmallSearchView.as_view(
        template_name="learn.html"), name='learn'),
    url(r'^about/?$', SmallSearchView.as_view(
        template_name="about.html"), name='about'),
    url(r'^agencies/?$', agencies, name='agencies'),
    url(r'^developers/?$', SmallSearchView.as_view(
        template_name="developers.html"), name='developers'),
    # Add in the singular version as well.
    url(r'^developer/?$', SmallSearchView.as_view(
        template_name="developers.html"), name='developer'),
    url(r'^contacts/(?P<slug>[-\w]+)/?$', contact_landing,
        name='contact_landing'),
    url(r'^documents/', include('docusearch.urls')),
    url(r'^request/noop/$', request_noop, name='noop'),
    url(r'^request/(?P<slug>[-\w]+)/$', request_form, name='form'),
    url(r'^robots\.txt$',
        TemplateView.as_view(
            template_name='robots.txt', content_type='text/plain')),
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

# Contact updater
urlpatterns += patterns(
    '',
    url(r'^update-contacts/', include(contact_updater_urls)),
)

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
