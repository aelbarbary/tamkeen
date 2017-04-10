from django.db import models
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import User


class Parent(User):
    gender = models.CharField(max_length=1, choices=(('M', 'Male',), ('F', 'Female',)))
    phone = models.CharField(max_length=10)
    other_phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100, null=True)
    def __str__(self):
        return 'Name: ' + self.name

class Child(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=(('M', 'Male',), ('F', 'Female',)))
    email = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    grade = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField()
    parent = models.ForeignKey(Parent, related_name='children')
    ethnic = models.CharField(max_length=20, choices=(('AA', 'African American',), ('NA', 'Native American',),('AN', 'Alaska Native',),('A', 'Asian',),('CW', 'Caucasian/White',),('HL', 'Hispanic/latino',),('PI', 'Pacific Islander',),('O', 'Other',)))
    
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
    image = models.ImageField(upload_to = "question", default = 'no-img.jpg')
    link = models.CharField(max_length=2000)
    closed = models.BooleanField('closed:')
    def __str__(self):
        return 'Name: ' + self.text

class QuestionAnswer(models.Model):
    answer = models.CharField(max_length=2000)
    name = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
