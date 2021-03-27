from django.contrib import admin

from cars.models import Manufacturer, Car

admin.site.register(Manufacturer)
admin.site.register(Car)
