from django.db import DataError, IntegrityError
from django.test import TestCase

from cars.models import Manufacturer


class ManufacturerTestWithoutDBConnection(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer()

    def test_manufacturer_instance(self):
        self.assertTrue(isinstance(self.manufacturer, Manufacturer))

    def test_manufacturer_proper_fields(self):
        self.assertEqual(
            [*self.manufacturer.__dict__],
            ["_state", "id", "make"]
        )

    def test_manufacturer_id_field(self):
        self.assertEqual(self.manufacturer.id, None)

    def test_manufacturer_empty_make_field(self):
        self.assertEqual(self.manufacturer.make, None)

    def test_manufacturer_make_field(self):
        manufacturer = Manufacturer(make="Ford")
        self.assertEqual(manufacturer.make, "Ford")

    def test_manufacturer_str(self):
        self.assertEqual(self.manufacturer.__str__(), self.manufacturer.make)


class ManufacturerTestWithDBConnection(TestCase):

    def test_manufacturer_create_with_proper_fields(self):
        manufacturer = Manufacturer.objects.create(make="Ford")
        self.assertNotEqual(manufacturer.id, None)
        self.assertEqual(manufacturer.make, "Ford")

    def test_manufacturer_empty_make_field(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create()

    def test_manufacturer_too_long_make_field(self):
        with self.assertRaises(DataError):
            Manufacturer.objects.create(make="t" * 151)
