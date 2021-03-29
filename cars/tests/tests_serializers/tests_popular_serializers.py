from django.db.models import Count
from django.test import TestCase

from cars.models import Manufacturer, Car, Rate
from cars.serializers import PopularSerializer


class PopularSerializersTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(make="Ford")
        self.car = Car.objects.create(manufacturer=self.manufacturer, model="Mustang")

        Rate.objects.create(car=self.car, rating=5)
        Rate.objects.create(car=self.car, rating=1)

        self.serializer_input = Car.objects.select_related("manufacturer").all().annotate(
            rates_number=Count("rate__rating")
        ).order_by("-rates_number")

        self.serializer = PopularSerializer(data=self.serializer_input, many=True)
        self.serializer.is_valid()

    def test_contain_expected_fields(self):
        data = self.serializer.data[0]
        self.assertCountEqual(data.keys(), ["id", "make", "model", "rates_number"])

    def test_contain_expected_values(self):
        data = self.serializer.data[0]
        self.assertEqual(data["id"], self.car.id)
        self.assertEqual(data["make"], self.manufacturer.make)
        self.assertEqual(data["model"], self.car.model)
        self.assertEqual(data["rates_number"], 2)
