"""
Definition of models.
"""

from django.db import models

class Job(models.Model):
    user = models.CharField(max_length=128)
    userID = models.CharField(max_length=64)
    job = models.CharField(max_length=128)
    timestamp = models.DateTimeField()
    priority = models.IntegerField(default=1000)
    state = models.CharField(max_length=32)

    def __str__(self):
        return self.user + " - " + self.job