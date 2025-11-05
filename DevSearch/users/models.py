from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100)
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
        return str(self.username)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.name} - ({self.owner.name})"
    
    class Meta:
        ordering = ['owner', '-description']
        
