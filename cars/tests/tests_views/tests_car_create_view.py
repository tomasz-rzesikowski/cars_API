from unittest.mock import patch

from django.db import DataError
from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from cars.models import Car, Manufacturer
from cars.serializers import CarGetSerializer

factory = APIRequestFactory()


class CarCreateViewTest(APITestCase):
    def setUp(self) -> None:
        self.view = CarListCreateView.as_view()
        self.url = reverse("cars:cars")

        self.external_API_Response = {
            "Count": 431,
            "Message": "Response returned successfully",
            "SearchCriteria": "Make:ford",
            "Results": [
                {"Make_ID": 474, "Make_Name": "FORD", "Model_ID": 1861, "Model_Name": "Mustang"},
                {"Make_ID": 474, "Make_Name": "FORD", "Model_ID": 1863, "Model_Name": "F-150"}
            ]
        }

    def test_url_revers(self):
        found = resolve(self.url)

        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(self.url, "/cars/")

    def test_empty_car_create(self):
        request = factory.post(self.url)

        response = self.view(request)
        response.render()

        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_model_and_manufacturer_not_in_db_car_post(self):
        """ Manufacturer and model doesn't exist in db."""
        request = factory.post(self.url, {"make": "Ford", "model": "Mustang"}, format="json")

        with self.assertRaises(DataError):
            Manufacturer.objects.get(make="Ford")

        with self.assertRaises(DataError):
            Car.objects.get(model="Mustang")

        with patch("cars.serializers.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = self.external_API_Response

            response = self.view(request)
            response.render()

        car = Car.objects.get(model="Mustang")
        serializer = CarGetSerializer(car)

        manufacturer = Manufacturer.objects.get(make="Ford")

        self.assertEqual(manufacturer.make, "Ford")
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_model_not_in_db_car_post(self):
        """ Manufacturer already exists in db. Model doesn't exist in db."""
        request = factory.post(self.url, {"make": "Ford", "model": "Mustang"}, format="json")

        Manufacturer.objects.create(make="Ford")

        with self.assertRaises(DataError):
            Car.objects.get(model="Mustang")

        with patch("cars.serializers.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = self.external_API_Response

            response = self.view(request)
            response.render()

        car = Car.objects.get(model="Mustang")
        serializer = CarGetSerializer(car)

        manufacturer_count = Manufacturer.objects.all().count()

        self.assertEqual(manufacturer_count, 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_model_and_manufacturer_in_db_car_post(self):
        """ Manufacturer and model already exist in db."""
        request = factory.post(self.url, {"make": "Ford", "model": "Mustang"}, format="json")

        manufacturer = Manufacturer.objects.create(make="Ford")
        Car.objects.create(manufacturer=manufacturer, model="Mustang")

        with patch("cars.serializers.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = self.external_API_Response

            response = self.view(request)
            response.render()

        car = Car.objects.get(model="Mustang")
        serializer = CarGetSerializer(car)

        manufacturer_count = Manufacturer.objects.all().count()
        car_count = Car.objects.all().count()

        self.assertEqual(manufacturer_count, 1)
        self.assertEqual(car_count, 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_model_and_manufacturer_not_in_external_API_car_post(self):
        """ Manufacturer and model doesn't exist in external API."""
        request = factory.post(self.url, {"make": "Honda", "model": "Civic"}, format="json")

        with patch("cars.serializers.requests.get") as mock_get:
            mock_get.return_value.ok = False

            response = self.view(request)
            response.render()

        with self.assertRaises(DataError):
            Manufacturer.objects.get(make="Honda")

        with self.assertRaises(DataError):
            Car.objects.get(model="Civic")

        self.assertEqual(response.data, {"detail": "Car not found in external API"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
