from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from books.tasks import send_registration_email

@receiver(post_save, sender=User)
def send_registration_email_signal(sender, instance, created, **kwargs):
    if created:
        send_registration_email.delay(instance.email)
