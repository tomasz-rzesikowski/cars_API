from django.test import TestCase

from cars.models import Manufacturer, Car, Rate
from cars.serializers import CarGetSerializer


class CarGetSerializersTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(make="Ford")
        self.car = Car.objects.create(manufacturer=self.manufacturer, model="Mustang")
        Rate.objects.create(car=self.car, rating=5)
        self.rate = Rate.objects.create(car=self.car, rating=1)
        self.serializer = CarGetSerializer(self.car)

    def test_contain_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["id", "make", "model", "avg_rating"])

    def test_contain_expected_values(self):
        data = self.serializer.data
        self.assertEqual(data["id"], self.car.id)
        self.assertEqual(data["make"], self.manufacturer.make)
        self.assertEqual(data["model"], self.car.model)
        self.assertEqual(data["avg_rating"], 3)
