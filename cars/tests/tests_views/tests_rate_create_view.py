from django.urls import resolve
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from cars.models import Car, Manufacturer, Rate
from cars.serializers import RateSerializer

factory = APIRequestFactory()


class RateListViewTest(APITestCase):
    def setUp(self) -> None:
        self.view = RateCreateView.as_view()
        self.url = reverse("cars:rate")
        manufacturer = Manufacturer.objects.create(make="Ford")
        self.car_id = Car.objects.create(manufacturer=manufacturer, model="Mustang")

    def test_url_revers(self):
        found = resolve(self.url)

        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(self.url, "/rate/")

    def test_empty_rate_create(self):
        request = factory.post(self.url)

        response = self.view(request)
        response.render()

        self.assertEqual(response.data, {'car_id': [ErrorDetail(string='This field is required.')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_proper_rate_create(self):
        manufacturer = Manufacturer.objects.create(make="Ford")
        car_id = Car.objects.create(manufacturer=manufacturer, model="Mustang")

        request = factory.post(self.url, {"car_id": car_id, "rating": 5}, format="json")
        response = self.view(request)
        response.render()

        rate = Rate.objects.last()
        rates = Rate.objects.all()
        serializer = RateSerializer(rate)

        self.assertEqual(len(rates), 1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rate_with_too_big_rating_create(self):
        manufacturer = Manufacturer.objects.create(make="Ford")
        car_id = Car.objects.create(manufacturer=manufacturer, model="Mustang")

        request = factory.post(self.url, {"car_id": car_id, "rating": 6}, format="json")
        response = self.view(request)
        response.render()

        self.assertEqual(response.data, {'rating': [ErrorDetail(string='Less then 5')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_with_too_small_rating_create(self):
        manufacturer = Manufacturer.objects.create(make="Ford")
        car_id = Car.objects.create(manufacturer=manufacturer, model="Mustang")

        request = factory.post(self.url, {"car_id": car_id, "rating": 0}, format="json")
        response = self.view(request)
        response.render()

        self.assertEqual(response.data, {'rating': [ErrorDetail(string='Greater then 0')]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
