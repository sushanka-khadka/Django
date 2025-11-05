from django.shortcuts import render
from django.db.models import Q
from .models import Project

# Create your views here.
def projects(request):
    # projects = Project.objects.all()
    search_query = request.GET.get('search_query')
    search_query = search_query if search_query else ''

    projects = Project.objects.filter(
        Q(title__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(owner__name__icontains = search_query) 
    )
    
    
    return render(request, 'projects/projects.html', {'projects': projects})


def project(request, pk):
    project = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project' : project})


def createProject(request):
    return render(request, 'projects/project-form.html')
def updateProject(request, pk):
    return render(request, 'projects/project-form.html')
def deleteProject(request, pk):
    pass