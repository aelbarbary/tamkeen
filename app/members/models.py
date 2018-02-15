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
import urllib.parse as urlparse

from .email import EmailSender

class Quiz(models.Model):
    name = models.CharField(max_length=2000)
    date_time = models.DateTimeField(blank=True, default=datetime.now)
    def __str__(self):
        return 'Name: ' + self.name


class Question(models.Model):
    text = models.CharField(max_length=2000)
    image = models.ImageField(upload_to = "question", default = 'no-img.jpg')
    video_link = models.CharField(max_length=2000, blank=True)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    def __str__(self):
        return 'Name: ' + self.text

class Profile(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    phone = models.CharField(max_length=20, blank=True)
    dob = models.DateField(max_length=8)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
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
        'phone': self.phone,
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
            subject = 'New Member'
            recepients = ['abdelrahman.elbarbary@gmail.com']

            message = "Tamkeener: %s %s\n" % (instance.first_name, instance.last_name)
            message += "Email: %s\n" % instance.email
            message += "Phone: %s" % instance.phone

            EmailSender(instance, subject, message, recepients).start()

post_save.connect(Profile.post_save, sender=Profile)

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
    if born:
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    else:
        return 'unknown'

class Answer(models.Model):
    text = models.CharField(max_length=2000)
    date_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

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
    hardcopy_available = models.BooleanField(default=False)
    def __str__(self):
         return '%s %s' % (self.name, self.description)

    @staticmethod
    def json(book):
        if book['book_file']:
            book_url = book['book_file']
            book_url_display = "inline"
        else:
            book_url = "#"
            book_url_display = "none"
        return {
        'id' : book['id'],
        'name': book['name'],
        'description': book['description'],
        'cover_page': book['cover_page'],
        'category': book['category'],
        'status': book['status'],
        'number_of_pages': book['number_of_pages'],
        'language' : book['language'],
        'book_file': book_url,
        'page_num': book['page_num'],
        'book_url_display': book_url_display,
        'hardcopy_available': book['hardcopy_available'],
        'holds' : book['holds']
        }

class BookReserve(models.Model):
    user = models.ForeignKey(Profile, related_name='user', on_delete=models.CASCADE,)
    book = models.ForeignKey(Book, related_name='book_reserves', on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    @staticmethod
    def post_save(sender, created, **kwargs):
        print("book reserved")
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
            message += "Phone: %s\n" % user.phone

            recepients = ['abdelrahman.elbarbary@gmail.com', 'alinour64@yahoo.com']
            EmailSender(instance, subject, message, recepients).start()

post_save.connect(BookReserve.post_save, sender=BookReserve)

class Attendance(models.Model):
    user = models.ForeignKey(Profile, related_name='attendance_user', on_delete=models.CASCADE,)
    date_time = models.DateTimeField()
    def __str__(self):
         return '%s %s' % (self.date_time, self.user)


class Checkout(models.Model):
    user = models.ForeignKey(Profile, related_name='checkout_user', on_delete=models.CASCADE,)
    date_time = models.DateTimeField()
    def __str__(self):
         return '%s %s' % (self.date_time, self.user)

class NewMemberRequest(models.Model):
    first_name =models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    gender = models.CharField(max_length=1, default="M")
    phone = models.CharField(max_length=10, blank=True, verbose_name= 'Phone Number')
    email = models.CharField(max_length=100, blank=False)
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Inquiry(models.Model):
    name =models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    text = models.TextField(verbose_name= 'Message')
    date_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return '%s %s' % (self.name, self.text)

class Award(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    prize = models.CharField(max_length=200, blank=True)
    pic=models.ImageField(upload_to='awards', default = 'awards/default.png' )
    def __str__(self):
        return '%s' % (self.name)

class UserAward(models.Model):
    user = models.ForeignKey(Profile, related_name='award_user',on_delete=models.CASCADE,)
    award = models.ForeignKey(Award, related_name='award', on_delete=models.CASCADE)
    description = models.TextField()
    date_time = models.DateTimeField()

class SuggestedVideo(models.Model):
    video = models.CharField(max_length=500, blank=False)
    video_id = models.CharField(max_length=12, blank=True, editable=False)
    date_time= models.DateTimeField()
    views = models.IntegerField(default=0, editable=False)
    def __str__(self):
        return '%s-%s' % (self.video, self.video_id)

    def save(self, *args, **kwargs):
        if self.video:
            parsed = urlparse.urlparse(self.video)
            print(urlparse.parse_qs(parsed.query)['v'][0])
            self.video_id = urlparse.parse_qs(parsed.query)['v'][0]
            super().save(*args, **kwargs)

class Alert(models.Model):
    user = models.ForeignKey(Profile, related_name='alert_user',on_delete=models.CASCADE,)
    level = models.CharField(max_length=10, blank=False)
    text = models.CharField(max_length=1000, blank=False)
    date_time = models.DateTimeField()
    dismissed = models.BooleanField(default=False)
