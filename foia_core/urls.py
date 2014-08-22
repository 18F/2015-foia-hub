from django.conf.urls import patterns, include, url
from django.conf import settings  # For debugging.
from django.contrib import admin
from django.views.generic import TemplateView

from foia_core.api import *


# Front-end
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.jinja"), name='home'),
)

# APIs
urlpatterns += patterns('',
    url(r'^api/agency/(?P<slug>[-\w]+)/$', include(OfficeResource.urls())),
    url(r'^api/agency/', include(AgencyResource.urls())),
    url(r'^api/request/', include(FOIARequestResource.urls())),
)

# Admin
admin.autodiscover()
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# For development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
