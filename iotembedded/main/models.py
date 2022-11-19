import datetime
from enum import unique
from tokenize import Name
from django.db import models
from django.contrib.auth.models import User

class userDetails(models.Model):
    user = models.ForeignKey(User, null = True, on_delete=models.PROTECT)
    Name = models.CharField(max_length = 50)
    UserID = models.IntegerField(unique=True)
    email = models.CharField(max_length = 100)
    def __str__(self):
        return f"Name:{self.Name}"

# Create your models here.
class device(models.Model):
    DeviceOwner = models.ForeignKey(userDetails, on_delete=models.PROTECT)
    deviceName = models.CharField(max_length = 20)
    deviceStatus = models.BooleanField()
    deviceID = models.IntegerField(unique=True) #True - On   False - Off
    def __str__(self):
        return f"Device Name:{self.deviceName} "

class sensor(models.Model):
    UserID = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    data = models.FloatField(blank=False)


