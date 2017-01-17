from django.db import models
from django.conf import settings

class Youth(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    image = models.ImageField(upload_to = "pic_folder", default = 'pic_folder/no-img.jpg')
