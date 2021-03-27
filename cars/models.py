from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, null=False, default=None)

    def __str__(self):
        return self.name


class Car(models.Model):
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.CASCADE, null=False)
    model = models.CharField(max_length=150, null=False, default=None)

    def __str__(self):
        return f"{self.manufacturer.name} {self.model}"
