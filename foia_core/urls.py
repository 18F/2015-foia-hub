from django.conf.urls import patterns, include, url
from django.conf import settings  # For debugging.

from django.views.generic import CreateView

from foia_core.forms import FOIARequestForm
# from foia_core.api import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),


    url(r'^request/?$', CreateView.as_view(
        form_class=FOIARequestForm,
        template_name="foia_core/generic_form.html"
        ),
        name='request-form',
        ),

    # url(r'^api/agency/(?P<slug>[-\w]+)/$', include(OfficeResource.urls())),
    # url(r'^api/agency/', include(AgencyResource.urls())),
    #url(r'^api/request/', include(FOIARequestResource.urls())),
)


# For development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
