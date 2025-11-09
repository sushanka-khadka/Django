from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(default='User hasn\'t set bio yet.', null=True, blank=True)
    profile_image = models.ImageField(default='profiles/user-default.png', null=True, blank=True, upload_to='profiles/')
    social_github = models.URLField(max_length=200, null=True, blank=True)
    social_linkedin = models.URLField(max_length=200, null=True, blank=True)
    social_twitter = models.URLField(max_length=200, null=True, blank=True)
    social_youtube = models.URLField(max_length=200, null=True, blank=True)
    social_website = models.URLField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return (str(self.first_name) + ' ' + str(self.last_name)) if self.last_name else str(self.first_name)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.name} - ({self.owner})"
    
    class Meta:
        ordering = ['owner', '-description']
        

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)       # sender can send message anonymously, so null and blank are True
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')    # message history matters, so we messages are preserved even if recipient profile is deleted
    sender_name = models.CharField(max_length=100, null=True, blank=True)   # if sender profile is deleted
    sender_email = models.EmailField(max_length=200, null=True, blank=True)      # in case sender is anonymous
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return str(self.subject)
    
    class Meta:
        ordering = ['is_read', '-created']