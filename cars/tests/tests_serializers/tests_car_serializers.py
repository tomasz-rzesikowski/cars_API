from django.test import TestCase

from cars.models import Manufacturer, Car


class ManufacturerSerializersTest(TestCase):

    def setUp(self):
        self.serializer_data = {
            "make": "Ford",
            "model": "Mustang"
        }

        self.manufacturer = Manufacturer.objects.create(name="Ford")
        self.car = Car.objects.create(manufacturer=self.manufacturer, model="Mustang")
        self.serializer = CarSerializer(self.car)

    def test_contain_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["make", "model"])

    def test_contain_expected_values(self):
        data = self.serializer.data
        self.assertEqual(data["make"], self.manufacturer.make)
        self.assertEqual(data["model"], self.car.model)

    def test_too_long_make_data(self):
        self.serializer_data["make"] = "t" * 151
        serializer = CarSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["make"])

    def test_too_long_model_data(self):
        self.serializer_data["model"] = "t" * 151
        serializer = CarSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["model"])
