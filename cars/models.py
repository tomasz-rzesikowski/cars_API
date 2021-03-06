from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Manufacturer(models.Model):
    make = models.CharField(max_length=150, null=False, default=None)

    def __str__(self):
        return self.make


class Car(models.Model):
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.CASCADE, null=False)
    model = models.CharField(max_length=150, null=False, default=None)

    def __str__(self):
        return f"{self.manufacturer.make} {self.model}"


class Rate(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE, null=False, related_name="rate")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False)

    def __str__(self):
        return f"{self.car.model} rating: {self.rating}"
