from django.db import DataError, IntegrityError
from django.test import TestCase

from cars.models import Manufacturer, Car


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
        manufacturer=Manufacturer(id=1, name="Ford")
        car = Car(manufacturer=manufacturer, model="Mustang")
        self.assertEqual(car.__str__(), "Ford Mustang")


class CarTestWithDBConnection(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Ford")
        self.car = Car.objects.create(model="Mustang", manufacturer=self.manufacturer)

    def test_car_create_with_proper_fields(self):
        self.assertNotEqual(self.car.id, None)
        self.assertEqual(self.car.model, "Mustang")
        self.assertEqual(self.car.manufacturer_id, self.manufacturer.id)

    def test_car_empty_manufacturer_id_field(self):
        with self.assertRaises(IntegrityError):
            Car.objects.create(model="Ford")

    def test_car_empty_model_field(self):
        with self.assertRaises(IntegrityError):
            Car.objects.create(manufacturer=self.manufacturer)

    def test_car_too_long_model_field(self):
        with self.assertRaises(DataError):
            Car.objects.create(manufacturer=self.manufacturer, model="t" * 151)

    def test_car_manufacturer_cascade_on_del(self):
        self.manufacturer.delete()
        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(pk=self.car.id)
