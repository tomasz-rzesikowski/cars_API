from rest_framework import serializers

from cars.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = ("make", )
