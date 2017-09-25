from django.db import models
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Question(models.Model):
    text = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    image = models.ImageField(upload_to = "question", default = 'no-img.jpg')
    video_link = models.CharField(max_length=2000, blank=True)
    closed = models.BooleanField('closed:')
    def __str__(self):
        return 'Name: ' + self.text

class QuestionAnswer(models.Model):
    answer = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
    # user = models.ForeignKey(User)
