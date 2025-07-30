from django.db import models

# Create your models here.

class Author(models.Model):
    fname= models.CharField(max_length=100)
    lname= models.CharField(max_length=100, blank=True)
    email_address = models.EmailField()

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Tag(models.Model):
    caption = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.caption}"

class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    # img_name = models.CharField(max_length=100)
    image= models.ImageField(upload_to='posts', null=True)
    date = models.DateField(auto_now= True)    
    slug = models.CharField(max_length=40, unique=True, db_index=True)
    content= models.TextField()
    author = models.ForeignKey(Author, null= True, on_delete=models.SET_NULL)      # one to many relation with author
    tags = models.ManyToManyField(Tag)    # many to  many relatioin with tags

    def __str__(self):
        return f"{self.title} ({self.date})"
    
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    # post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # one to many relation with post
    post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # one to many relation with post
    # related_name Gives a custom, readable name for reverse relation default is 'post_set'

    def __str__(self):
        return f"{self.name} commented \"{self.comment}\""

