import requests
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from cars.models import Manufacturer, Car, Rate


class CarGetSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source="manufacturer", max_length=150)
    avg_rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ("id", "make", "model", "avg_rating")


class CarPostSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source="manufacturer", max_length=150)

    class Meta:
        model = Car
        fields = ("make", "model")

    def create(self, validated_data):
        """Create or get Manufacturer and Car"""
        manufacturer_make = validated_data["manufacturer"]
        car_model = validated_data["model"]

        imported_data = self.get_from_externaL_API(manufacturer_make)

        for car in imported_data.json()["Results"]:
            if car_model == car["Model_Name"]:
                man = Manufacturer.objects.get_or_create(make=manufacturer_make)[0]
                instance = Car.objects.get_or_create(manufacturer=man, model=car_model)[0]

                return instance

        raise NotFound(detail="Car not found in external API")

    def get_from_externaL_API(self, manufacturer_make):
        import_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{manufacturer_make}?format=json"
        return requests.get(import_url)


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ("car_id", "rating")


class PopularSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source="manufacturer", max_length=150)
    rates_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ("id", "make", "model", "rates_number")
