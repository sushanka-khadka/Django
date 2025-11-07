from django import forms
from .models import Project, Review

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['owner']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        
        # placeholder text for body field
        widgets = {            
            'body': forms.Textarea(attrs={'placeholder':'Share your thoughts...'}),
        }                                         


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

