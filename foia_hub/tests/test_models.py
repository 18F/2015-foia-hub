from django.test import SimpleTestCase, TestCase

from foia_hub.models import Agency, Office


class AgencyTests(SimpleTestCase):
    def test_common_requests_field(self):
        """Verify that we can treat a JSONField as a list"""
        agency = Agency(name='Dr. Suess',
                        common_requests=['Thing one', 'Thing two', 'Red Fish'])
        agency.save()
        # Serialized to the DB and back again
        retrieved = Agency.objects.get(pk=agency.pk)
        self.assertEqual(retrieved.common_requests,
                         ['Thing one', 'Thing two', 'Red Fish'])
        agency.delete()

    def test_agency_save(self):
        agency = Agency(name='Department of Transportation')
        agency.save()

        retrieved = Agency.objects.get(pk=agency.pk)
        self.assertEqual(
            'Agency: Department of Transportation', str(retrieved))
        self.assertEqual(retrieved.slug, 'department-of-transportation')

    def test_office_save(self):
        agency = Agency(name='Department of Commerce')
        agency.save()

        office = Office(name='Commerce Is FUNdamental', agency=agency)
        office.save()
        retrieved = Office.objects.get(pk=office.pk)

        self.assertEqual(retrieved.office_slug, 'commerce-is-fundamental')
        self.assertEqual(retrieved.slug, 'department-of-commerce--commerce-is-fundamental')


class MoreAgencyTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_get_all_offices(self):
        agency = Agency.objects.get(slug='department-of-commerce')
        all_offices = agency.get_all_offices()
        names = [a.name for a in all_offices]
        self.assertTrue('U.S. Patent and Trademark Office' in names)
        self.assertTrue('Census Bureau' in names)
