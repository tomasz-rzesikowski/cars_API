from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from cars.models import Car, Manufacturer, Rate
from cars.serializers import PopularSerializer
from cars.views import PopularListView

factory = APIRequestFactory()


class PopularListViewTest(APITestCase):
    def setUp(self) -> None:
        self.view = PopularListView.as_view()
        self.request = factory.get(reverse("cars:list_popular"))

    def test_url_revers(self):
        url = reverse("cars:list_popular")
        found = resolve(url)

        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(url, "/popular/")

    def test_empty_popular_list(self):
        cars = Car.objects.all()
        serializer = PopularSerializer(cars, many=True)

        response = self.view(self.request)
        response.render()

        self.assertCountEqual(response.data, [])
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_empty_popular_list(self):
        manufacturer = Manufacturer.objects.create(make="Ford")

        car_one = Car.objects.create(manufacturer=manufacturer, model="Mustang")
        car_two = Car.objects.create(manufacturer=manufacturer, model="F-150")

        Rate.objects.create(car=car_one, rating=1)
        Rate.objects.create(car=car_one, rating=5)

        Rate.objects.create(car=car_two, rating=4)

        cars = Car.objects.all()
        serializer = PopularSerializer(cars, many=True)

        response = self.view(self.request)
        response.render()

        self.assertCountEqual(response.data[0].keys(), ["id", "make", "model", "rates_number"])
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data[0]["rates_number"], 2)
        self.assertEqual(response.data[1]["rates_number"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
