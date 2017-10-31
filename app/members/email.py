import threading
from datetime import date
from django.core.mail import send_mail

class EmailSender(threading.Thread):
    def __init__(self, instance, subject, message, recepients):
        threading.Thread.__init__(self)
        self.instance = instance
        self.subject = subject
        self.message = message
        self.recepients = recepients

    def run(self):
        try:
            send_mail(
                self.subject,
                self.message,
                'tamkeen.website@gmail.com',
                self.recepients,
                fail_silently=False,
            )
        except Exception as e:
            print(e)
