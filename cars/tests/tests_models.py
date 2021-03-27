from django.core.exceptions import ValidationError
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
            ["_state", "id", "name"]
        )

    def test_manufacturer_id_field(self):
        self.assertEqual(f"{self.manufacturer.id}", "None")

    def test_manufacturer_name_field(self):
        manufacturer = Manufacturer(name="Ford")
        self.assertEqual(f"{manufacturer.name}", "Ford")

    def test_manufacturer_str(self):
        self.assertEqual(self.manufacturer.__str__(), self.manufacturer.name)


class ManufacturerTestWithDBConnection(TestCase):

    def test_manufacturer_proper_name_field(self):
        manufacturer = Manufacturer.objects.create(name="Ford")
        self.assertNotEqual(manufacturer.id, None)
        self.assertEqual(manufacturer.name, "Ford")

    def test_manufacturer_empty_name_field(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create()

    def test_manufacturer_too_long_name_field(self):
        with self.assertRaises(DataError):
            Manufacturer.objects.create(name="t" * 151)
