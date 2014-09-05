from django.db import models

# Create your models here.

class URL(models.Model):
    short_url = models.TextField()
    long_url = models.TextField()
