from rest_framework import serializers

from cars.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source="name", max_length=150)

    class Meta:
        model = Manufacturer
        fields = ("make", )
