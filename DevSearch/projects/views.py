from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .utils import searchProject, paginateProject
from .forms import ProjectForm

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

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.title = project.title.title()

            form.save()     # save the new project instance
            messages.success(request, 'Project created successfully.')
            return redirect('my-account')
    return render(request, 'projects/project-form.html', {'form':form})


@login_required(login_url='login')
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.title = project.title.title()
             
            # Save the updated project instance
            form.save() # or project.save()            
            
            messages.success(request, 'Project updated successfully.')
            return redirect('my-account')
    return render(request, 'projects/project-form.html', {'form':form})

@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('my-account')
    
    return render(request, 'delete-template.html', {'object':project, 'type':'project'})