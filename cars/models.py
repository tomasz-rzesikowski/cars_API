from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, null=False, default=None)

    def __str__(self):
        return self.name
