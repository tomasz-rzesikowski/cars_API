from django.contrib import admin

from cars.models import Manufacturer, Car, Rate

admin.site.register(Manufacturer)
admin.site.register(Car)
admin.site.register(Rate)
