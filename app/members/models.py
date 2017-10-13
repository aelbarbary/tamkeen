from django.db import models
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class Quiz(models.Model):
    name = models.CharField(max_length=2000)

class Question(models.Model):
    text = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    image = models.ImageField(upload_to = "question", default = 'no-img.jpg')
    video_link = models.CharField(max_length=2000, blank=True)
    quiz = models.ForeignKey(Quiz, related_name='questions')
    def __str__(self):
        return 'Name: ' + self.text

class Profile(AbstractUser):
    whats_app = models.CharField(max_length=20, blank=True)
    dob = models.DateField(max_length=8)

    @staticmethod
    def post_save(sender, **kwargs):
        try:
            print("post save")
            instance = kwargs.get('instance')
            created = kwargs.get('created')
            message = "%s %s: %s" % (instance.first_name, instance.last_name, instance.whats_app)
            send_mail(
                'New Member',
                message,
                'abdelrahman.elbarbary@gmail.com',
                ['abdelrahman.elbarbary@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(e) 

post_save.connect(Profile.post_save, sender=Profile)

class Answer(models.Model):
    text = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers')
    user = models.ForeignKey(Profile)
