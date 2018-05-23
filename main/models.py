from django.db import models


class Monitor(models.Model):
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=500, default="Default Monitor Name")

    def __str__(self):
        return self.url