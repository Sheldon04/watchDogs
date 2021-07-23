from django.db import models

# Create your models here.
from django.db import models
from system.storage import ImageStorage

# Create your models here.

class mypicture(models.Model):
    phone = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='photos', default='', storage=ImageStorage())

class invationRecord(models.Model):
    date = models.DateField()
    time = models.TimeField()
    level = models.IntegerField()
    camera_id = models.IntegerField()
    area = models.CharField(max_length= 50)
    invation_num =models.IntegerField()