from django.db import models

# Create your models here.
class Range(models.Model):
    dummy = models.CharField(default="This is dumb", max_length=32,null=True)