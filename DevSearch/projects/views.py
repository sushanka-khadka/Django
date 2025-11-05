from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    )   # # projects as a queryset from Project model

    page = request.GET.get('page')
    page = page if page else 1    # Default to page 1 if no page is specified

    results = 3
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)     # Get the projects for the requested page
    except PageNotAnInteger:
        page = 1    # If page is not an integer, deliver the first page.
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # If page is out of range, deliver last page of results.
        projects = paginator.page(page)
    
    context = {'projects': projects, 'paginator': paginator}    # # projects as paginated object (not queryset from Project model)

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