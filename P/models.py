from django.db import models
from django.utils import timezone


# Create your models here.
class Userlogin(models.Model):
    userid = models.CharField(max_length=122, default='1')
    password = models.CharField(max_length=122, default='prithiv')
    

class Visitor(models.Model):
     name = models.CharField(max_length=50)
     city = models.CharField(max_length=50, default='unknown')
     phone = models.CharField(max_length=50)
     host = models.CharField(max_length=50)
     purpose = models.CharField(max_length=255)
     vehiclenum = models.CharField(max_length=25, default='unknown')
     visit_time = models.DateTimeField(default=timezone.now)

class park_vehicle(models.Model):
     vehiclenumber = models.CharField(max_length=255)
     intime = models.CharField(max_length=255, default='unknown')
     seatnum = models.CharField(max_length=10)
     exit = models.CharField(max_length=10)
