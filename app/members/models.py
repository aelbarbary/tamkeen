from django.db import models
from django.conf import settings
from PIL import Image

class Youth(models.Model):
    name = models.CharField(max_length=200)

    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male',), ('F', 'Female',)))
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100, null=True)
    guardian_email = models.CharField(max_length=200)
    guardian_phone = models.CharField(max_length=10)
    interests = models.CharField(max_length=1000)
    skills = models.CharField(max_length=1000)
    rank = models.IntegerField(default=1)
    image = models.ImageField(upload_to = "youth", default = 'no-img.jpg')

    def __str__(self):
        return 'Name: ' + self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    date_time = models.DateTimeField()
    address = models.CharField(max_length=100)
    price = models.IntegerField()
    registeration_link = models.CharField(max_length=500)
    flyer = models.ImageField(upload_to = "event", default = 'no-img.jpg')
    gender = models.BooleanField('Gender:')
    def __str__(self):
        return 'Name: ' + self.name

class EventImages(models.Model):
    image = models.ImageField(upload_to = "event", default = 'no-img.jpg')
    description = models.CharField(max_length=1000)
    event = models.ForeignKey(Event, related_name='images')

class Question(models.Model):
    text = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    closed = models.BooleanField('closed:')
    def __str__(self):
        return 'Name: ' + self.text

class QuestionAnswer(models.Model):
    answer = models.CharField(max_length=2000)
    name = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
