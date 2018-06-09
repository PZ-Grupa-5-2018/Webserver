from django.contrib import admin

from .models import Monitor, MyUser

admin.site.register(MyUser)
admin.site.register(Monitor)