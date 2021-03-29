from django.db.models import Avg
from django.test import TestCase

from cars.models import Manufacturer, Car, Rate
from cars.serializers import CarGetSerializer


class CarGetSerializersTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(make="Ford")
        self.car = Car.objects.create(manufacturer=self.manufacturer, model="Mustang")

        Rate.objects.create(car=self.car, rating=5)
        Rate.objects.create(car=self.car, rating=1)

        self.serializer_input = Car.objects.select_related("manufacturer").all().annotate(
            avg_rating=Avg("rate__rating")
        )

        self.serializer = CarGetSerializer(data=self.serializer_input, many=True)
        self.serializer.is_valid()

    def test_contain_expected_fields(self):
        data = self.serializer.data[0]
        self.assertCountEqual(data.keys(), ["id", "make", "model", "avg_rating"])

    def test_contain_expected_values(self):
        data = self.serializer.data[0]
        self.assertEqual(data["id"], self.car.id)
        self.assertEqual(data["make"], self.manufacturer.make)
        self.assertEqual(data["model"], self.car.model)
        self.assertEqual(data["avg_rating"], 3)
