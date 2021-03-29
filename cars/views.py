from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, DestroyAPIView

from cars.models import Car
from cars.serializers import CarGetSerializer, PopularSerializer, CarPostSerializer


class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarGetSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = CarPostSerializer
        return super().create(request)


class CarDeleteView(DestroyAPIView):
    serializer_class = CarGetSerializer
    queryset = Car.objects.all()


class PopularListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = PopularSerializer

    def list(self, request, *args, **kwargs):
        serializer = super().list(request)

        serializer_data = sorted(serializer.data, key=lambda x: x["rates_number"], reverse=True)
        return Response(serializer_data)
