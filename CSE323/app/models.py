"""
Definition of models.
"""

from django.db import models

class Job(models.Model):
    id = models.CharField(max_length=64)
    user = models.CharField(max_length=128)
    job = models.CharField(max_length=128)
    timestamp = models.DateTimeField()
    time_req = models.TimeField()