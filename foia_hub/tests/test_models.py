from django.test import SimpleTestCase, TestCase

from foia_hub.models import Agency, Office, Stats

from foia_hub.scripts.load_agency_contacts import add_stats

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

    def test_add_stats(self):
        """ Confirms that records listed as `none` are not loaded """
        #load data
        agency = Agency.objects.get(name='Department of Transportation')
        test_yaml_data = {'request_time_stats':{'2013':{}}}
        test_yaml_data['request_time_stats']['2013']\
            .update({'Simple-Median No. of Days':'21'})
        test_yaml_data['request_time_stats']['2013']\
            .update({'Complex-Median No. of Days':None})
        test_yaml_data['request_time_stats']['2012'] = \
            {'Simple-Median No. of Days':'1'}
        add_stats(test_yaml_data, agency)

        #verify latest data is returned when it exists
        retrieved = agency.stats_set.filter(stat_type = 'S') \
            .order_by('-year').first()
        self.assertEqual(retrieved.median, 21)

        #verify that any medians equal to `none` were not loaded
        retrieved = agency.stats_set.filter(stat_type = 'C') \
            .order_by('-year').first()
        self.assertEqual(retrieved, None)
        with self.assertRaises(AttributeError) as error:
            retrieved.median
        self.assertEqual(type(error.exception), AttributeError )
