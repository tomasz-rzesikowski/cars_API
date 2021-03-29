from django.urls import resolve
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from cars.models import Car, Manufacturer
from cars.views import CarDeleteView

factory = APIRequestFactory()


class CarDelViewTest(APITestCase):
    def setUp(self) -> None:
        self.view = CarDeleteView.as_view()
        self.reverse_url = reverse("cars:car_del", kwargs={"pk": 1})
        self.base_url = "/cars/"
        self.request = factory.delete(self.base_url)
        self.manufacturer = Manufacturer.objects.create(make="Ford")

    def test_url_reverse(self):
        found = resolve(self.reverse_url)

        self.assertEqual(found.func.__name__, self.view.__name__)
        self.assertEqual(self.reverse_url, "/cars/1/")

    def test_existing_car_del(self):
        car_id = Car.objects.create(manufacturer=self.manufacturer, model="Mustang").id

        response = self.view(self.request, pk=car_id)
        response.render()

        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(pk=car_id)

        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_existing_car_del(self):

        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(pk=1)

        response = self.view(self.request, pk=1)
        response.render()

        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
