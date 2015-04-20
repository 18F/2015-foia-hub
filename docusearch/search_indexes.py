from haystack import indexes

from .models import Document


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    """ The Haystack related class that defined what's going to be indexed. """

    # This uses a template, but essentially indexes the extracted text of a
    # document.
    text = indexes.CharField(document=True, use_template=True)

    # We'll very likely want to facet on the agency, name. This adds an index
    # that enables that.
    foia_agency = indexes.CharField(
        model_attr='release_agency_slug', faceted=True)

    date_released = indexes.DateField(model_attr='date_released', null=True)

    def get_model(self):
        return Document
