from django.apps import AppConfig
from .model import *
from django.db.models.signals import post_save

class MembersConfig(AppConfig):
    name = 'members'
    post_save.connect(Profile.post_save, sender=Profile)
    post_save.connect(BookReserve.post_save, sender=BookReserve)
