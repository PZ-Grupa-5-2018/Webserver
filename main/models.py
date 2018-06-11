import re

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def validate_url(value):
    reg = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if not reg.match(value):
        raise ValidationError("The URL {} is incorrect.".format(value))


class Monitor(models.Model):
    url = models.CharField(max_length=500, validators=[validate_url])
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.url.endswith('/'):
            self.url += '/'
        super(Monitor, self).save(*args, **kwargs)


class CustomMeasurement(models.Model):
    owner = models.ForeignKey(
        User,
        unique=False,
        # false dlatego ze jeden user moze miec wiele custom measurementow
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=250, blank=False, default='Custom Measurement')
    url = models.CharField(max_length=250, blank=False, default='')
    host_id = models.CharField(max_length=250, default='')
    monitor_id = models.CharField(max_length=250, default='')
    created = models.DateTimeField(default=timezone.now())
