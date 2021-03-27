from django.db import DataError, IntegrityError
from django.test import TestCase

from cars.models import Manufacturer


class CarTestWithoutDBConnection(TestCase):

    def setUp(self):
        self.car = Car()

    def test_car_instance(self):
        self.assertTrue(isinstance(self.car, Car))

    def test_car_proper_fields(self):
        self.assertEqual(
            [*self.car.__dict__],
            ["_state", "id", "manufacturer_id", "model"]
        )

    def test_car_id_field(self):
        self.assertEqual(self.car.id, None)

    def test_car_empty_manufacturer_id_field(self):
        self.assertEqual(self.car.manufacturer_id, None)

    def test_car_empty_model_field(self):
        self.assertEqual(self.car.model, None)

    def test_car_manufacturer_id_field(self):
        car = Car(manufacturer_id=1)
        self.assertEqual(car.manufacturer_id, 1)

    def test_car_model_field(self):
        car = Car(model="Mustang")
        self.assertEqual(car.model, "Mustang")

    def test_car_str(self):
        self.assertEqual(self.car.__str__(), self.car.model)


class CarTestWithDBConnection(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Ford")

    def test_car_create_with_proper_fields(self):
        car = Car.objects.create(name="Mustang", manufacturer_id=self.manufacturer)
        self.assertNotEqual(car.id, None)
        self.assertEqual(car.model, "Mustang")
        self.assertEqual(car.manufacturer_id, self.manufacturer.id)

    def test_car_empty_manufacturer_id_field(self):
        with self.assertRaises(IntegrityError):
            Car.objects.create(model="Ford")

    def test_car_empty_model_field(self):
        with self.assertRaises(IntegrityError):
            Car.objects.create(manufacturer_id=self.manufacturer)

    def test_car_too_long_model_field(self):
        with self.assertRaises(DataError):
            Car.objects.create(manufacturer_id=self.manufacturer, name="t" * 151)
