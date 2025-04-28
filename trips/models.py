from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    activities = models.ManyToManyField(Activity)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    packing_list = models.TextField(null=True, blank=True)
    travel_tips = models.TextField(null=True, blank=True)



    def __str__(self):
        return f"{self.location} ({self.start_date} - {self.end_date})"
