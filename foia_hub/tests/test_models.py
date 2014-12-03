from django.test import SimpleTestCase, TestCase

from foia_hub.models import Agency, Office, Stats, ReadingRoomUrls


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
        self.assertEqual(
            retrieved.slug, 'department-of-commerce--commerce-is-fundamental')


class MoreAgencyTests(TestCase):
    fixtures = ['agencies_test.json', 'offices_test.json']

    def test_get_all_components(self):
        agency = Agency.objects.get(slug='department-of-commerce')
        all_offices = agency.get_all_components()
        names = [a.name for a in all_offices]
        self.assertTrue('U.S. Patent and Trademark Office' in names)
        self.assertTrue('Census Bureau' in names)


class StatsTest(SimpleTestCase):
    def test_statstest_save(self):
        """ Confirm obj saves and validate number handling. """
        agency = Agency(name='Department of Homeland Security')
        agency.save()

        stats = Stats(
            agency=agency,
            year=2014,
            stat_type='S',
            median=1.26,
        )
        stats.save()

        retrieved = Stats.objects.get(pk=stats.pk)
        self.assertEqual(retrieved.median, 1.26)
        self.assertEqual(retrieved.less_than_one, False)


class ReadingRoomUrlsTest(TestCase):
    def test_str_output(self):
        r = ReadingRoomUrls(link_text='Link One', url='http://one.gov')
        self.assertEqual(str(r), 'Link One http://one.gov')
