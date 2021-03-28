import requests
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from cars.models import Manufacturer, Car, Rate


class CarGetSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source="manufacturer", max_length=150)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ("id", "make", "model", "avg_rating")

    def get_avg_rating(self, obj):
        return Rate.objects.filter(car_id=obj.id).aggregate(Avg("rating")).get("rating__avg")


class CarPostSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source="manufacturer", max_length=150)

    class Meta:
        model = Car
        fields = ("make", "model")

    def create(self, validated_data):
        """Create or get Manufacturer and Car"""
        manufacturer_make = validated_data["manufacturer"]
        car_model = validated_data["model"]

        import_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{manufacturer_make}?format=json"
        imported_data = requests.get(import_url)

        for car in imported_data.json()["Results"]:
            if car_model == car["Model_Name"]:
                man = Manufacturer.objects.get_or_create(make=manufacturer_make)[0]
                instance = Car.objects.get_or_create(manufacturer=man, model=car_model)[0]
                return instance

        raise NotFound(detail="Car not found in external API")


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ("car_id", "rating")
