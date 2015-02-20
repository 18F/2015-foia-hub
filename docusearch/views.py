from django.shortcuts import render

from haystack.query import SearchQuerySet

from .models import Document


def details(request, document_id):
    document = Document.objects.get(id=document_id)
    context = {'document': document}

    more_like_this = SearchQuerySet().more_like_this(document).models(Document)
    if more_like_this.count() > 10:
        more_like_this = more_like_this[1:9]

    context['similar_documents'] = more_like_this

    return render(request, 'docusearch/detail.html', context)
