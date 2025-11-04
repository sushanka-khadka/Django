from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    # user = 
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(default='User hasn\'t set bio yet.', null=True, blank=True)
    profile_image = models.ImageField(default='profiles/default.png', null=True, blank=True)
    social_github = models.URLField(max_length=200, null=True, blank=True)
    social_linkedin = models.URLField(max_length=200, null=True, blank=True)
    social_twitter = models.URLField(max_length=200, null=True, blank=True)
    social_youtube = models.URLField(max_length=200, null=True, blank=True)
    social_website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.username)




# user, name, email, username, loca, shor, bio, img, soc_git, link,, tw yt, web