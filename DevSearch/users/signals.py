from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# @receiver(signal=post_save, sender=User)
def createProfile(sender, instance, created, **kwargs): #  when a User instance is created, this function will be called
    print('\nSignal triggered')

    if created:     # if a new User instance is created
        user = instance
        profile = Profile.objects.create(
            user = user,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            username = user.username
        )   # profile instance created    

        profile.save()


# @receiver(signal=post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):    # when a Profile instance is updated, this user instance will also be updated
    profile = instance
    user = profile.user
    if created == False:
        try:
            user.first_name = profile.name
            user.email = profile.email if profile.email else ''
            user.username = profile.username
            user.save()    
        except Exception as e:
            print('Error updating user:', e)


# @receiver(signal=post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):        # created argument not needed as signal is post_delete
    profile = instance
    user = profile.user
    user.delete()   # when a Profile instance is deleted, user instance will also be deleted


#  use decorators or connect method to connect signals
post_save.connect(receiver=createProfile, sender=User)   # when User model is saved, createProfile function will be called
post_save.connect(receiver=updateUser, sender=Profile)   # when Profile model is saved, updateUser function will be called
post_delete.connect(receiver=deleteUser, sender=Profile)   # when Profile model is deleted, deleteUser function will be called