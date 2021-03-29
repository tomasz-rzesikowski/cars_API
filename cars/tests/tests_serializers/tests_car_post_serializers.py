from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import NotFound

from cars.models import Manufacturer, Car
from cars.serializers import CarPostSerializer


class ManufacturerSerializersTest(TestCase):

    def setUp(self):
        self.serializer_data = {
            "make": "Ford",
            "model": "Mustang"
        }

        self.external_API_Response = {
            "Count": 431,
            "Message": "Response returned successfully",
            "SearchCriteria": "Make:ford",
            "Results": [
                {"Make_ID": 474, "Make_Name": "FORD", "Model_ID": 1861, "Model_Name": "Mustang"},
                {"Make_ID": 474, "Make_Name": "FORD", "Model_ID": 1863, "Model_Name": "F-150"}
            ]
        }

        self.manufacturer = Manufacturer.objects.create(make="Ford")
        self.car = Car.objects.create(manufacturer=self.manufacturer, model="Mustang")
        self.serializer = CarPostSerializer(self.car)

    def test_contain_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["make", "model"])

    def test_contain_expected_values(self):
        data = self.serializer.data
        self.assertEqual(data["make"], self.manufacturer.make)
        self.assertEqual(data["model"], self.car.model)

    def test_too_long_make_data(self):
        self.serializer_data["make"] = "t" * 151
        serializer = CarPostSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["make"])

    def test_too_long_model_data(self):
        self.serializer_data["model"] = "t" * 151
        serializer = CarPostSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["model"])

    def test_save_proper_request(self):
        serializer = CarPostSerializer(data=self.serializer_data)

        serializer.is_valid()
        with patch("cars.serializers.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = self.external_API_Response
            self.assertEqual(serializer.save(), self.car)

    def test_save_not_existed_car_request(self):
        self.serializer_data["model"] = "unknown"
        with self.assertRaises(NotFound):
            serializer = CarPostSerializer(data=self.serializer_data)
            serializer.is_valid()

            with patch("cars.serializers.requests.get") as mock_get:
                mock_get.return_value.ok = False
                serializer.save()
