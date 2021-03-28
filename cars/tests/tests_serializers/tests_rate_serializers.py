from django.test import TestCase

from cars.models import Manufacturer, Car, Rate
from cars.serializers import RateSerializer


class RateSerializersTest(TestCase):

    def setUp(self):
        self.serializer_data = {
            "car_id": 1,
            "rating": 1
        }

        self.manufacturer = Manufacturer.objects.create(make="Ford")
        self.car = Car.objects.create(manufacturer=self.manufacturer, model="Mustang")
        self.rate = Rate.objects.create(car=self.car, rating=1)
        self.serializer = RateSerializer(self.rate)

    def test_contain_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["car_id", "rating"])

    def test_contain_expected_values(self):
        data = self.serializer.data
        self.assertEqual(data["car_id"], self.rate.car_id)
        self.assertEqual(data["rating"], self.rate.rating)

    def test_too_small_rating_data(self):
        self.serializer_data["rating"] = 0
        serializer = RateSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["rating"])

    def test_too_big_rating_data(self):
        self.serializer_data["rating"] = 6
        serializer = RateSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["rating"])
