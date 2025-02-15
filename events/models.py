from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description= models.TextField()
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Participant,related_name="events")


    def __str__(self):
        return self.name