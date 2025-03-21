from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name



class Event(models.Model):
    name = models.CharField(max_length=200)
    description= models.TextField()
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="events")
    asset=models.ImageField(upload_to='events_asset', blank=True,null=True,default="events_asset/default_img.jpg")



    def __str__(self):
        return self.name