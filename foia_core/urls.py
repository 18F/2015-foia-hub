from django.conf.urls import patterns, include, url
from django.conf import settings  #For debugging.

from django.views.generic import CreateView

from foia_core.forms import FOIARequestForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foia_core.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),


    url(r'^request/?$', CreateView.as_view(
    	form_class=FOIARequestForm,
        template_name="foia_core/generic_form.html"
        ),
	    name='request-form',
	)
)


# For development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

