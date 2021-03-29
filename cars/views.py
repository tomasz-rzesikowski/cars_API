from django.db.models import Avg, Count, Func

from rest_framework.generics import ListAPIView, ListCreateAPIView, DestroyAPIView, CreateAPIView

from cars.models import Car
from cars.serializers import CarGetSerializer, PopularSerializer, CarPostSerializer, RateSerializer


class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.select_related("manufacturer").all().annotate(
        avg_rating=Func(Avg("rate__rating"), 2, function="ROUND"))
    serializer_class = CarGetSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CarPostSerializer
        return super().create(request)


class CarDeleteView(DestroyAPIView):
    serializer_class = CarGetSerializer
    queryset = Car.objects.all()


class PopularListView(ListAPIView):
    queryset = Car.objects.select_related("manufacturer").all().annotate(
        rates_number=Count("rate__rating")).order_by("-rates_number")
    serializer_class = PopularSerializer


class RateCreateView(CreateAPIView):
    serializer_class = RateSerializer
