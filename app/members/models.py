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
    title = models.CharField(max_length=100, default='TAMKEENER')
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
        'age': calculate_age(self.dob),
        'skills': self.skills,
        'title': self.title
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
    description = models.TextField(blank=True, null=True)
    cover_page = models.ImageField(upload_to='books', default = 'books/default.png' )
    category = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=2, blank=False, default='A')
    number_of_pages = models.IntegerField(default=0)
    language = models.CharField(max_length=2, default="en")
    book_file = models.FileField(upload_to="books")
    page_num = models.IntegerField(default=0)

    def __str__(self):
         return '%s %s' % (self.name, self.description)

    @property
    def json(self):
        if self.book_file:
            book_url = self.book_file.url
            book_url_display = "inline"
        else:
            book_url = "#"
            book_url_display = "none"
        return {
        'id' : self.id,
        'name': self.name,
        'description': self.description,
        'cover_page': self.cover_page.url,
        'category': self.category,
        'status': self.status,
        'number_of_pages': self.number_of_pages,
        'language' : self.language,
        'book_file': book_url,
        'page_num': self.page_num,
        'book_url_display': book_url_display
        }

class BookReserve(models.Model):
    user = models.ForeignKey(Profile, related_name='user')
    book = models.ForeignKey(Book, related_name='book_reserves')
    date_time = models.DateTimeField()
