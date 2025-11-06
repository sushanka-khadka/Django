from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# @receiver(signal=post_save, sender=User)
def createProfile(instance, created, **kwargs):
    print('\nSignal triggered')

    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            name = user.first_name + ' ' + user.last_name,
            email = user.email,
            username = user.username
        )   # profile instance created    


post_save.connect(receiver=createProfile, sender=User)   # when User model is saved, createProfile function will be called