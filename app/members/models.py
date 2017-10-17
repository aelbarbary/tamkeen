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
import threading
from datetime import date

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
    gender = models.CharField(max_length=1, default='M')
    photo = models.ImageField(upload_to='profile_pics', default = 'profile_pics/default.png' )
    uw_waiver = models.ImageField(upload_to='uw_waivers', default = 'uw_waivers/default.png')
    skills = models.TextField(blank=True, null=True)
    notes =  models.TextField(blank=True, null=True)
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def json(self):
        return {
        'first_name': self.first_name,
        'last_name': self.last_name,
        'email': self.email,
        'whats_app': self.whats_app,
        'gender': self.gender,
        'uw_waiver': self.uw_waiver.url,
        'photo': self.photo.url,
        'age': calculate_age(self.dob)
        }

    @staticmethod
    def post_save(sender, created, **kwargs):
        if created:
            instance = kwargs.get('instance')
            SendEmail(instance, sender).start()

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class SendEmail(threading.Thread):
    def __init__(self, instance, sender):
        threading.Thread.__init__(self)
        self.instance = instance
        self.sender = sender

    def run(self):
        try:

            message = "%s %s: %s" % (self.instance.first_name, self.instance.last_name, self.instance.whats_app)
            send_mail(
                'New Member',
                message,
                'tamkeen.website@gmail.com',
                ['abdelrahman.elbarbary@gmail.com', 'haythamlion@outlook.com'],
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

class Book(models.Model):
    name = models.CharField(max_length=200, blank=False)
    cover_page = models.ImageField(upload_to='books', default = 'books/default.png' )
    category = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=1, blank=False, default='A')

class BookCheckoutRequest(models.Model):
    user = models.ForeignKey(Profile, related_name='user')
    book = models.ForeignKey(Book, related_name='book')
    date_time = models.DateTimeField()
