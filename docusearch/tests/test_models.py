import datetime
from django.test import TestCase
from datetime import date
from docusearch.models import Document, upload_original_to


class DocumentTests(TestCase):
    def test_document_creation(self):
        """ A simple check to ensure a document can be created correctly. """

        doc = Document()
        doc.text = "This is the full-text of the document"
        doc.title = "Useful Document"
        doc.release_agency_slug = "department-of-justice--information"
        doc.date_created = datetime.date(2017, 5, 4)
        doc.date_released = datetime.date(2017, 5, 5)
        doc.pages = 100
        doc.file_type = 'xlsx'

        doc.save()

        saved = Document.objects.get(title='Useful Document')
        self.assertEqual(saved.text, "This is the full-text of the document")
        self.assertEqual(datetime.date(2017, 5, 5), saved.date_released)
        self.assertEqual(datetime.date(2017, 5, 4), saved.date_created)
        self.assertEqual(100, saved.pages)
        self.assertEqual('xlsx', saved.file_type)

    def test_upload_original_to(self):
        """ Ensure the upload_original_to() returns a correct path. """

        doc = Document()
        doc.text = "This is the full-text of the document"
        doc.title = "Useful Document"
        doc.release_agency_slug = "department-of-justice--information"
        doc.date_released = date.today()

        doc.save()

        upload_path = upload_original_to(doc, 'test.PDF')
        self.assertTrue(upload_path.startswith(
            'department-of-justice/information'))
        self.assertTrue('test.pdf' in upload_path)

    def test_get_absolute_url(self):
        """ Test the get_absolute_url method for the Document object. """

        doc = Document()
        doc.text = "This is the full-text of the document"
        doc.title = "Useful Document"
        doc.release_agency_slug = "department-of-justice--information"
        doc.date_released = date.today()
        doc.save()

        url = doc.get_absolute_url()
        self.assertEqual(url, '/documents/document/%s' % doc.id)
