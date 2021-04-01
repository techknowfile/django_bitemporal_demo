from django.db.models import Prefetch
from django.test import TestCase
import datetime
from temporal.models import Foo, FooVersion, Bar, Baz, BazVersion
from graphene.test import Client
from temporal.schema import schema
from freezegun import freeze_time

FOO_QUERY = """
                        {
                          foos {
                            __typename
                            id
                            versions {
                              __typename
                              id
                              validStartDate
                              validEndDate
                              sysEndDate
                              
                              identity {
                                __typename
                                id
                              }
                              value
                            }
                            bars {
                              __typename
                              id
                              name
                              baz {
                                __typename
                                id
                                versions {
                                  __typename
                                  id
                                  validStartDate
                                  validEndDate
                                  sysEndDate
                                  
                                  identity {
                                    __typename
                                    id
                                  }
                                  value
                                }
                              }
                            }
                          }
                        }
            """

# Create your tests here.
class BitemporalTestCase(TestCase):
    def setUp(self):
        # Initialize foos
        self.foo1 = Foo.objects.create()
        self.foo2 = Foo.objects.create()

        # Initialize foo versions
        foo1_1 = self.foo1.versions.add_version(
            FooVersion(
                valid_start_date=datetime.datetime(2021, 1, 1).date(),
                valid_end_date=datetime.datetime.max.date(),
                value=0)
        )
        foo1_2 = self.foo1.versions.add_version(
            FooVersion(
                valid_start_date=datetime.datetime(2021, 2, 1).date(),
                valid_end_date=datetime.datetime(2021, 3, 1).date(),
                value=0)
        )

        # Initialize bars
        self.bar1 = Bar.objects.create(foo=self.foo1, name="foo1_bar1")
        self.bar2 = Bar.objects.create(foo=self.foo1, name="foo1_bar2")

        # Initialize baz
        self.baz1 = self.bar1.baz.create()

        # Initialize baz versions
        self.baz1.versions.add_version(
            BazVersion(
                valid_start_date=datetime.datetime(2021, 1, 1).date(),
                valid_end_date=datetime.datetime.max.date(),
                value=0))

    def test_foo_versions_created(self):
        foo1 = self.foo1
        # All versions at all times
        self.assertEqual(foo1.versions.count(), 4)

        # All current versions
        self.assertEqual(foo1.versions.current().count(), 3)

    def test_replace_all_current_versions(self):
        foo1 = self.foo1
        foo1.versions.add_version(
            FooVersion(
                valid_start_date=datetime.datetime(2021, 1, 1).date(),
                valid_end_date=datetime.datetime.max.date(),
                value=0)
        )

        self.assertEqual(foo1.versions.current().count(), 1)

    def test_baz_versions_created(self):
        baz1 = self.baz1
        # All versions at all times
        self.assertEqual(baz1.versions.count(), 1)

        # All current versions
        self.assertEqual(baz1.versions.current().count(), 1)

    def test_nested_temporal_query(self):
        mark_start = datetime.datetime.now()
        self.foo1.versions.add_version(
            FooVersion(
                valid_start_date=datetime.datetime(2021, 1, 1).date(),
                valid_end_date=datetime.datetime.max.date(),
                value=0)
        )

        bar1 = self.foo1.bars.first()
        baz1 = bar1.baz.first()
        baz1_2 = baz1.versions.add_version(
            BazVersion(
                valid_start_date=datetime.datetime(2021, 1, 2).date(),
                valid_end_date=datetime.datetime.max.date(),
                value=0
            )
        )

        # Check initial state and current state directly (not prefetched)
        with self.assertNumQueries(4):
            self.assertEqual(self.foo1.versions.as_of(mark_start).count(), 3)
            self.assertEqual(self.foo1.bars.first().baz.first().versions.as_of(mark_start).count(), 1)

        with self.assertNumQueries(4):
            self.assertEqual(self.foo1.versions.current().count(), 1)
            self.assertEqual(self.foo1.bars.first().baz.first().versions.current().count(), 2)

        # Check initial state and current state using optimized manager (prefetched)
        with self.assertNumQueries(10):
            foo1_start = Foo.optimized.as_of(mark_start).all()[0]
            foo1_current = Foo.optimized.current().all()[0]

        with self.assertNumQueries(0):
            self.assertEqual(foo1_start.versions.count(), 3)
            self.assertEqual(foo1_start.bars.all()[0].baz.all()[0].versions.count(), 1)
        with self.assertNumQueries(0):
            self.assertEqual(foo1_current.versions.count(), 1)
            self.assertEqual(foo1_current.bars.all()[0].baz.all()[0].versions.count(), 2)

        # Test graphql client
        # This confirms that the backend query is running the minimum number of queries necessary
        with self.assertNumQueries(5):
            self.maxDiff = None
            client = Client(schema=schema)
            response = client.execute(FOO_QUERY)
            self.assertDictEqual(response,
                 {'data': {'foos': [{'__typename': 'Foo',
                    'id': '1',
                    'versions': [{'__typename': 'FooVersion',
                      'id': '5',
                      'validStartDate': '2021-01-01',
                      'validEndDate': '9999-12-31',
                      'sysEndDate': '9999-12-31T23:59:59.999999',
                      'identity': {'__typename': 'Foo', 'id': '1'},
                      'value': 0.0}],
                    'bars': [{'__typename': 'Bar',
                      'id': '1',
                      'name': 'foo1_bar1',
                      'baz': [{'__typename': 'Baz',
                        'id': '1',
                        'versions': [{'__typename': 'BazVersion',
                          'id': '1',
                          'validStartDate': '2021-01-01',
                          'validEndDate': '2021-01-02',
                          'sysEndDate': '9999-12-31T23:59:59.999999',
                          'identity': {'__typename': 'Baz', 'id': '1'},
                          'value': 0.0},
                         {'__typename': 'BazVersion',
                          'id': '3',
                          'validStartDate': '2021-01-02',
                          'validEndDate': '9999-12-31',
                          'sysEndDate': '9999-12-31T23:59:59.999999',
                          'identity': {'__typename': 'Baz', 'id': '1'},
                          'value': 0.0}]}]},
                     {'__typename': 'Bar', 'id': '2', 'name': 'foo1_bar2', 'baz': []}]},
                   {'__typename': 'Foo', 'id': '2', 'versions': [], 'bars': []}]}}
            )
