from django.test import SimpleTestCase

from foia_hub.models import Agency, Office, Stats


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


class StatsTest(SimpleTestCase):
    def test_statstest_save(self):
        """ Confirm obj saves and validate number handling. """
        agency = Agency(name='Department of Homeland Security')
        agency.save()

        stats = Stats(
            agency=agency,
            year=2014,
            stat_type='S',
            average=1.2666,
            median=1,
            )
        stats.save()

        retrieved = Stats.objects.get(pk=stats.pk)
        self.assertEqual(retrieved.low, None)
        self.assertEqual(retrieved.average, 1.2666)
        self.assertEqual(retrieved.median, 1)
