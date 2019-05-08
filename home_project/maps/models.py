from django.db import models

class address_info(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    data = models.CharField(max_length=200)
