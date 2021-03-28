from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from cars.models import Car, Manufacturer
from cars.serializers import CarGetSerializer

factory = APIRequestFactory()


class CarListViewTest(APITestCase):
    def test_url_revers(self):
        url = reverse("cars:cars_list")
        self.assertEqual(url, "/cars/")

    def test_empty_car_list(self):
        response = factory.get(reverse("cars:cars_list"))
        cars = Car.objects.all()
        serializer = CarGetSerializer(cars, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_empty_car_list(self):
        manufacturer = Manufacturer.objects.create(make="Ford")

        Car.objects.create(manufacturer=manufacturer, model="Mustang")
        Car.objects.create(manufacturer=manufacturer, model="F-150")

        response = factory.get(reverse("cars:cars_list"))
        cars = Car.objects.all()
        serializer = CarGetSerializer(cars, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
