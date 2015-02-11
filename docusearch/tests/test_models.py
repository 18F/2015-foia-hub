from django.test import TestCase

from docusearch.models import Document

class DocumentTests(TestCase):
    def test_document_creation(self):
        """ A simple check to ensure a document can be created correctly. """

        doc = Document()
        doc.text = "This is the full-text of the document"
        doc.title = "Useful Document"
        doc.release_agency_slug = "department-of-justice--information"
        doc.path = ('/store/documents/doj/22.pdf')

        doc.save()

        saved = Document.objects.get(title='Useful Document')
        self.assertEqual(saved.text, "This is the full-text of the document")
