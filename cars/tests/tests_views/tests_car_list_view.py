from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from cars.models import Car, Manufacturer
from cars.serializers import CarGetSerializer
from cars.views import CarListCreateView

factory = APIRequestFactory()


class CarListViewTest(APITestCase):
    def setUp(self) -> None:
        self.view_object = CarListCreateView()
        self.view = CarListCreateView.as_view()
        self.url = reverse("cars:cars")
        self.request = factory.get(self.url)

    def test_url_revers(self):
        found = resolve(self.url)

        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(self.url, "/cars/")

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

        cars = self.view_object.get_queryset()
        serializer = CarGetSerializer(cars, many=True)

        response = self.view(self.request)
        response.render()

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
