from django.db import models
from django.conf import settings
from PIL import Image

class Youth(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField(null=True)
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100, null=True)
    guardian_email = models.CharField(max_length=200)
    guardian_phone = models.CharField(max_length=10)
    interests = models.CharField(max_length=1000)
    skills = models.CharField(max_length=1000)
    rank = models.IntegerField()
    image = models.ImageField(upload_to = "youth", default = 'pic_folder/no-img.jpg')

    def __str__(self):
        return 'Name: ' + self.name

    def save(self):

        if not self.id and not self.image:
            return

        super(Youth, self).save()

        image = Image.open(self.image)
        (width, height) = image.size

        "Max width and height 800"
        if (200 / width < 200 / height):
            factor = 200 / height
        else:
            factor = 200 / width

        size = ( width / factor, height / factor)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

class Note(models.Model):
    youth_id = models.IntegerField()
    note = models.CharField(max_length=1000)
    date_time = models.DateTimeField()

class Volunteer(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField()
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    interests = models.CharField(max_length=1000)
    skills = models.CharField(max_length=1000)
    image = models.ImageField(upload_to = "volunteer", default = 'pic_folder/no-img.jpg')

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    date_time = models.DateTimeField()
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to = "event", default = 'pic_folder/no-img.jpg')
