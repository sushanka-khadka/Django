from django.db import models
import uuid

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
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

    @property       # to access as an attribute(project.reviewers) instead of method (project.reviewers())
    def reviewers(self):
        # filter review that doesn't have owner (in case owner profile is deleted)
        available_reviewers = self.review_set.filter(owner__isnull=False)   # avoid NoneType error
        return available_reviewers.values_list('owner__id', flat=True)  # get list of reviewer(profile) ids for this project
    
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        totalVotes = reviews.count()
        upVotes = reviews.filter(value='up').count()

        self.vote_total = totalVotes
        self.vote_ratio = int(upVotes / totalVotes * 100)  if totalVotes > 0 else 0     # avoid division by zero    
    
class Review(models.Model):
    Vote_Type = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=Vote_Type)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.project.title} - {self.value}'
    
    class Meta:
        # unique_together = [['owner', 'project']]  # one review per user per project
        ordering = ['-created']  # latest review first

    

class Tag(models.Model):
    name = models.CharField(max_length=200)    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
