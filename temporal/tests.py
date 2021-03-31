from django.db.models import Prefetch
from django.test import TestCase
import datetime
from temporal.models import Foo, FooVersion, Bar, Baz, BazVersion


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
            foo1_start = Foo.optimized.as_of(mark_start).first()
            foo1_current = Foo.optimized.current().first()

        with self.assertNumQueries(0):
            self.assertEqual(foo1_start.versions.count(), 3)
            self.assertEqual(foo1_start.bars.all()[0].baz.all()[0].versions.count(), 1)
        with self.assertNumQueries(0):
            self.assertEqual(foo1_current.versions.count(), 1)
            self.assertEqual(foo1_current.bars.all()[0].baz.all()[0].versions.count(), 2)
