from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
# from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
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

        # variables for email
        subject = 'Welcome to DevSearch'
        message = '''Hi {profile.first_name},\n\nThank you for registering at DevSearch.
        \nYour login credentials are:\nUsername: {profile.username}
        \nBest regards,\nDevSearch Team'''.format(profile=profile)

        from_email = settings.EMAIL_HOST_USER
        to_emails = [profile.email]      # mustn't be empty list else email won't be sent

        # sending email on user creation 
        try:
            send_mail(
                subject,
                message,
                from_email,
                to_emails,  # email won't be sent if to_emails is empty even in console backend
                fail_silently=False,        # Set to False to raise exceptions on failure (default is True for silent failure on production).
            )
            print('\nEmail sent successfully to', profile.email)
        except Exception as e:
            print('\nError sending welcome email:', e)            
            

# @receiver(signal=post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):    # when a Profile instance is updated, this user instance will also be updated
    profile = instance
    user = profile.user
    if created == False:
        try:
            user.first_name = profile.first_name
            user.last_name = profile.last_name if profile.last_name else ''
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