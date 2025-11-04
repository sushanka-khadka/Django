from django.db import models
import uuid

# Create your models here.
class Project(models.Model):
    # owner
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    feature_image = models.ImageField(null=True, blank=True, default="projects/default.jpg", upload_to="projects/")
    source_link = models.URLField(max_length=200, null=True, blank=True)
    demo_link = models.URLField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)


class Review(models.Model):
    Vote_Type = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # owner 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=Vote_Type)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return str(self.value)
    

class Tag(models.Model):
    name = models.CharField(max_length=200)    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
