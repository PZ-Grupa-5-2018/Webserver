from django.contrib import admin

from .models import Monitor, CustomMeasurement

admin.site.register(CustomMeasurement)
admin.site.register(Monitor)