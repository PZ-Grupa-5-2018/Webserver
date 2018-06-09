from django.db import models


class Monitor(models.Model):
    url = models.CharField(max_length=500)
    #name = models.CharField(max_length=500, default="Default Monitor Name")

    def __str__(self):
        return self.url


class MyUser(models.Model):
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, blank=False, null=False)
    active = models.BooleanField(default=True)

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def is_active(self):
        return self.active
