from django.db import models

# Create your models here.


class Work_entry(models.Model):
    position = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    time = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.position