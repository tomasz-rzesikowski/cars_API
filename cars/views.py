from rest_framework.generics import ListAPIView

from cars.models import Car
from cars.serializers import CarGetSerializer


class CarListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarGetSerializer
