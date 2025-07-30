from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ['name', 'email', 'comment']
        # fields = '__all__'
        exclude = ['post']  # Exclude the post field as it will be set in the view
        
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'comment': 'Your Comment',
        }
