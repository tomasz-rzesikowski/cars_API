from requests import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView


from cars.models import Car
from cars.serializers import CarGetSerializer, PopularSerializer, CarPostSerializer


class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarGetSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = CarPostSerializer(request.data)
        return Response(serializer.data)


# class CarCreateView(APIView):
#     def post(self, request, format=None):
#
#         return Response()


class PopularListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = PopularSerializer
