from django.test import TestCase

from cars.models import Manufacturer
from cars.serializers import ManufacturerSerializer


class ManufacturerSerializersTest(TestCase):

    def setUp(self):
        self.manufacturer_attributes = {
            "name": "Ford"
        }
        self.serializer_data = {
            "make": "Ford"
        }

        self.manufacturer = Manufacturer.objects.create(**self.manufacturer_attributes)
        self.serializer = ManufacturerSerializer(self.manufacturer)

    def test_contain_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["make"])

    def test_contain_expected_values(self):
        data = self.serializer.data
        self.assertEqual(data["make"], self.manufacturer.name)

    def test_too_long_manufacturer_name_data(self):
        self.serializer_data["make"] = "t"*151
        serializer = ManufacturerSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["make"])
