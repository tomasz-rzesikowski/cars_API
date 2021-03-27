from django.db import DataError, IntegrityError
from django.test import TestCase

from cars.models import Manufacturer, Car


class RatingTestWithoutDBConnection(TestCase):

    def setUp(self):
        self.rate = Rate()

    def test_rate_instance(self):
        self.assertTrue(isinstance(self.rate, Rate))

    def test_rate_proper_fields(self):
        self.assertEqual(
            [*self.rate.__dict__],
            ["_state", "id", "car_id", "rating"]
        )

    def test_rate_id_field(self):
        self.assertEqual(self.rate.id, None)

    def test_rate_empty_car_id_field(self):
        self.assertEqual(self.rate.car_id, None)

    def test_rate_empty_rating_field(self):
        self.assertEqual(self.rate.rating, None)

    def test_rate_car_id_field(self):
        rate = Rate(car_id=1)
        self.assertEqual(rate.car_id, 1)

    def test_rate_model_field(self):
        rate = Rate(rating=5)
        self.assertEqual(rate.rating, 5)

    def test_rate_str(self):
        car = Car(id=1, model="Mustang")
        rate = Rate(car=car, rating=4)
        self.assertEqual(rate.__str__(), "Mustang rating: 4")


class RatingTestWithDBConnection(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Ford")
        self.car = Car.objects.create(manufacturer=self.manufacturer, model="Mustang")
        self.rate = Rate.objects.create(car=self.car, rating=3)

    def test_rate_create_with_proper_fields(self):
        self.assertNotEqual(self.rate.id, None)
        self.assertEqual(self.rate.car_id, self.car.id)
        self.assertEqual(self.rate.rating, 3)

    def test_rate_empty_car_id_field(self):
        with self.assertRaises(IntegrityError):
            Rate.objects.create(rate=3)

    def test_rate_empty_rating_field(self):
        with self.assertRaises(IntegrityError):
            Rate.objects.create(car=self.car)

    def test_rate_too_small_value_rating_field(self):
        with self.assertRaises(DataError):
            Rate.objects.create(car=self.car, rating=0)

    def test_rate_too_big_value_rating_field(self):
        with self.assertRaises(DataError):
            Rate.objects.create(car=self.car, rating=6)

    def test_rate_manufacturer_cascade_on_del(self):
        self.car.delete()
        with self.assertRaises(Rate.DoesNotExist):
            Rate.objects.get(pk=self.rate.id)
