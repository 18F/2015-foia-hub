import os
from django.shortcuts import render
from django.http import QueryDict

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory

from .models import Document


def details(request, document_id):
    document = Document.objects.get(id=document_id)
    context = {'document': document}

    more_like_this = SearchQuerySet().more_like_this(document).models(Document)
    if more_like_this.count() > 10:
        more_like_this = more_like_this[1:9]

    context['similar_documents'] = more_like_this

    return render(request, 'docusearch/detail.html', context)


class CustomSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = FacetedSearchForm

        super(CustomSearchView, self).__init__(*args, **kwargs)

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['selected_facets'] = self.request.GET.getlist(
            "selected_facets")

        return super(CustomSearchView, self).build_form(form_kwargs)

    def clean_query(self, old_query=None):
        """
        Creates a clean query string to prevent duplicate GET queries
        from entering request
        """
        if not old_query:
            old_query = self.request.GET

        clean_query = QueryDict('', mutable=True)
        clean_query.update(old_query)

        if clean_query.get('order_by'):
            del clean_query['order_by']

        return clean_query.urlencode()

    def extra_context(self):
        extra = super(CustomSearchView, self).extra_context()
        extra['request'] = self.request
        extra['facets'] = self.results.facet_counts()
        extra['cleaned_query'] = self.clean_query()
        return extra


def search(request):

    sqs = SearchQuerySet().models(Document).highlight().facet('foia_agency')

    if request.GET.get('order_by') == 'date_released':
        sqs = sqs.order_by('date_released')

    view = search_view_factory(
        view_class=CustomSearchView,
        template='search/search.html',
        searchqueryset=sqs,
        form_class=FacetedSearchForm,
    )
    return view(request)
