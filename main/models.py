import re

from django.core.exceptions import ValidationError
from django.db import models


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
