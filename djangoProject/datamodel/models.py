from django.db import models

# Create your models here.
from django.db import models
from system.storage import ImageStorage

# Create your models here.

class mypicture(models.Model):
    phone = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='photos', default='', storage=ImageStorage())