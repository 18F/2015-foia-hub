from django.shortcuts import render

from haystack.query import SearchQuerySet

from .models import Document

def details(request, document_id):
    document = Document.objects.get(id=document_id)
    context = {'document': document}

    return render(request, 'docusearch/detail.html', context)
