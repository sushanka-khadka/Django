from django.shortcuts import render, HttpResponse

from .models import Project

# Create your views here.
def projects(request):    
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': projects})


def project(request, pk):
    return render(request, 'projects/single-project.html')
def createProject(request):
    return render(request, 'projects/project-form.html')
def updateProject(request, pk):
    return render(request, 'projects/project-form.html')
def deleteProject(request, pk):
    pass