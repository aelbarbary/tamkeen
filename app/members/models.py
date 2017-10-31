from django.db import models
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime, timedelta, time

from .email import EmailSender

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
        'id' : self.id,
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

    @property
    def json_attendace(self):
         return {
         'id' : self.id,
         'first_name': self.first_name,
         'last_name': self.last_name,
         'gender': self.gender,
         'age': calculate_age(self.dob),
         'attended_today': get_attendace(self.id)
         }

    @staticmethod
    def post_save(sender, created, **kwargs):
        if created:
            instance = kwargs.get('instance')
            subject = 'New Member'
            recepients = ['abdelrahman.elbarbary@gmail.com']

            message = "Tamkeener: %s %s\n" % (instance.first_name, instance.last_name)
            message += "Email: %s\n" % instance.email
            message += "WhatsApp: %s" % instance.whats_app

            EmailSender(instance, subject, message, recepients).start()

def get_attendace(user_id):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    attendace = Attendance.objects.filter(user_id=user_id, date_time__lte=today_end, date_time__gte=today_start)
    if attendace:
        return True
    return False

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

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
    book_file = models.FileField(upload_to="books", blank=True)
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

    @staticmethod
    def post_save(sender, created, **kwargs):
        if created:
            instance = kwargs.get('instance')
            print(instance)
            user = instance.user
            book = instance.book

            subject = 'New Borrow Request'

            message = "Book Name: %s\n" % book.name
            message += "Description: %s\n" % book.description
            message += "Category: %s\n" % book.category
            message += "Tamkeener: %s %s\n" % (user.first_name, user.last_name)
            message += "Email: %s\n" % user.email
            message += "WhatsApp: %s\n" % user.whats_app

            recepients = ['abdelrahman.elbarbary@gmail.com', 'alinour64@yahoo.com']
            EmailSender(instance, subject, message, recepients).start()

class Attendance(models.Model):
    user = models.ForeignKey(Profile, related_name='attendance_user')
    date_time = models.DateTimeField()
