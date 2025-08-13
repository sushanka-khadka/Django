from django.db import models

# Create your models here.
class Meetup(models.Model):
    title = models.CharField(max_length=200)    # default: null=False, blank=False
    location = models.CharField(max_length=100, default='yet do decide')
    slug= models.SlugField(unique=True)
    description= models.TextField()
    featured_image= models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.title