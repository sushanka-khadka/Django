from django.shortcuts import render
from django.db.models import Q
from .models import Project, Tag
from .utils import searchProject, paginateProject

# Create your views here.
def projects(request):
    # projects = Project.objects.all()    
    projects, search_query = searchProject(request)   # projects as filtered queryset from Project model

    projects, custom_range = paginateProject(request, projects, results=6)   # paginated projects e.g page 1 of 5
    context = {'projects': projects, 'search_query':search_query, 'custom_range':custom_range}    # projects as paginated object (not queryset from Project model)

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project' : project})


def createProject(request):
    return render(request, 'projects/project-form.html')
def updateProject(request, pk):
    return render(request, 'projects/project-form.html')

def deleteProject(request, pk):
    pass