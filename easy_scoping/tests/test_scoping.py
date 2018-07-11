from django.test import TestCase
from widgets.models import Widget
from django.core import management as man


class ScopingTests(TestCase):

    def setUp(self):
        man.call_command('loaddata',
                         'tests/fixtures/filter_test_data.json')

    def test_db_data_loaded(self):
        obj = Widget.objects.all()
        self.assertEqual(obj.count(), 336)

    def test_passing_many_kwargs(self):
        obj1 = Widget.objects.filter(color='blue',
                                     size='small')
        obj2 = Widget.objects.all().take_kwargs(color='blue', size='small')

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())

        obj3 = Widget.objects.all().take_kwargs(size='small', color='blue')

        self.assertQuerysetEqual(obj1,
                                 obj3,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj3.count())

    def test_passing_kwargs(self):
        obj1 = Widget.objects.filter(color='blue')
        obj2 = Widget.objects.all().take_kwargs(color='blue')

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())

    def test_passing_many_args(self):
        obj1 = Widget.objects.filter(color='blue',
                                     size='small')
        obj2 = Widget.objects.all().take_more_args('blue', 'small')

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())

    def test_passing_args(self):
        obj1 = Widget.objects.filter(color='blue')
        obj2 = Widget.objects.all().take_args('blue')

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())

    def test_no_scope_registered(self):
        with self.assertRaises(AttributeError):
            Widget.objects.all().not_a_scope()

    def test_redundant_chain(self):
        obj1 = Widget.objects.all().basic_query_widget()
        obj2 = obj1.basic_query_widget()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())
        self.assertEqual(obj1.get(), obj2.get())

        not_obj1 = Widget.objects.all().not_basic_query_widget()
        not_obj2 = not_obj1.not_basic_query_widget()

        self.assertQuerysetEqual(not_obj1,
                                 not_obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(not_obj1.count(), not_obj2.count())

    def test_query_widget(self):
        obj1 = Widget.objects.filter(color='blue',
                                     size='small',
                                     shape='circle')
        obj2 = Widget.objects.all().basic_query_widget()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())
        self.assertEqual(obj1.get(), obj2.get())

        not_obj1 = Widget.objects.exclude(color='blue',
                                          size='small',
                                          shape='circle')
        not_obj2 = Widget.objects.all().not_basic_query_widget()

        self.assertQuerysetEqual(not_obj1,
                                 not_obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(not_obj1.count(), not_obj2.count())

    def test_query_chaining(self):
        obj1 = Widget.objects.filter(color='blue') \
                             .filter(size='small') \
                             .filter(shape='circle')
        obj2 = Widget.objects.all().blue().small().circle()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())
        self.assertEqual(obj1.get(), obj2.get())

        not_obj1 = Widget.objects.exclude(color='blue') \
                                 .exclude(size='small') \
                                 .exclude(shape='circle')
        not_obj2 = Widget.objects.all().not_blue().not_small().not_circle()

        self.assertQuerysetEqual(not_obj1,
                                 not_obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(not_obj1.count(), not_obj2.count())

    def test_query_blue(self):
        obj1 = Widget.objects.filter(color='blue')
        obj2 = Widget.objects.all().blue()

        self.assertEqual(obj1.count(), obj2.count())
        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)

        not_obj1 = Widget.objects.exclude(color='blue')
        not_obj2 = Widget.objects.all().not_blue()

        self.assertEqual(not_obj1.count(), not_obj2.count())
        self.assertQuerysetEqual(not_obj1,
                                 not_obj2,
                                 transform=lambda x: x,
                                 ordered=False)

    def test_before_y2k(self):
        import datetime

        obj1 = Widget.objects.filter(used_on__lte=datetime.date(2000, 1, 1))
        obj2 = Widget.objects.all().before_y2k()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())

        not_obj1 = Widget.objects.exclude(used_on__lte=datetime.date(2000, 1, 1))
        not_obj2 = Widget.objects.all().not_before_y2k()

        self.assertQuerysetEqual(not_obj1,
                                 not_obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(not_obj1.count(), not_obj2.count())

    def test_after_y2k(self):
        import datetime

        obj1 = Widget.objects.filter(used_on__gte=datetime.date(2000, 1, 1))
        obj2 = Widget.objects.all().after_y2k()

        self.assertQuerysetEqual(obj1,
                                 obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(obj1.count(), obj2.count())

        not_obj1 = Widget.objects.exclude(used_on__gte=datetime.date(2000, 1, 1))
        not_obj2 = Widget.objects.all().not_after_y2k()

        self.assertQuerysetEqual(not_obj1,
                                 not_obj2,
                                 transform=lambda x: x,
                                 ordered=False)
        self.assertEqual(not_obj1.count(), not_obj2.count())
