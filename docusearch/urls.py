from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView, search_view_factory

from .views import details
from .models import Document


sqs = SearchQuerySet().models(Document).highlight().facet('')

urlpatterns = patterns(
    'haystack.views',
    url(r'^$', TemplateView.as_view(template_name='search/index.html'), name="search_home"),
    url(
        r'^search/',
        search_view_factory(
            view_class=FacetedSearchView,
            template='search/search.html',
            searchqueryset=sqs,
            form_class=FacetedSearchForm,
        ),
        name='doc_search'),
    url(r'^document/(?P<document_id>\d+)/$', details, name="doc_details")
)
