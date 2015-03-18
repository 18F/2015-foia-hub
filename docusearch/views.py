from django.shortcuts import render

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView, search_view_factory

from .models import Document


def details(request, document_id):
    document = Document.objects.get(id=document_id)
    context = {'document': document}

    more_like_this = SearchQuerySet().more_like_this(document).models(Document)
    if more_like_this.count() > 10:
        more_like_this = more_like_this[1:9]

    context['similar_documents'] = more_like_this

    return render(request, 'docusearch/detail.html', context)


def search(request):

    sqs = SearchQuerySet().models(Document).highlight().facet('foia_agency')

    if request.GET.get('order_by') == 'date_released':
        sqs = sqs.order_by('date_released')

    view = search_view_factory(
        view_class=FacetedSearchView,
        template='search/search.html',
        searchqueryset=sqs,
        form_class=FacetedSearchForm
    )
    return view(request)
