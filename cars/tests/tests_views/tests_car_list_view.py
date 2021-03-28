from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from cars.models import Car, Manufacturer
from cars.serializers import CarGetSerializer
from cars.views import CarListView

factory = APIRequestFactory()


class CarListViewTest(APITestCase):
    def setUp(self) -> None:
        self.view = CarListView.as_view()
        self.request = factory.get(reverse("cars:list_cars"))

    def test_url_revers(self):
        url = reverse("cars:list_cars")
        found = resolve(url)

        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(url, "/cars/")

    def test_empty_car_list(self):
        cars = Car.objects.all()
        serializer = CarGetSerializer(cars, many=True)

        response = self.view(self.request)
        response.render()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_empty_car_list(self):
        manufacturer = Manufacturer.objects.create(make="Ford")

        Car.objects.create(manufacturer=manufacturer, model="Mustang")
        Car.objects.create(manufacturer=manufacturer, model="F-150")

        cars = Car.objects.all()
        serializer = CarGetSerializer(cars, many=True)

        response = self.view(self.request)
        response.render()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
