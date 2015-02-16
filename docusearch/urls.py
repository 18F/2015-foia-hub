from django.conf.urls import patterns, include, url

from docusearch.views import details


urlpatterns = patterns('',
    url(r'^document/(?P<document_id>\d+)/$', details, name="doc_details")
)
