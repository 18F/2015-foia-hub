from haystack import indexes

from .models import Document


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    foia_agency = indexes.CharField(
        model_attr='release_agency_slug', faceted=True)

    def get_model(self):
        return Document
