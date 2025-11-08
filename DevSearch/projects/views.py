from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .utils import searchProject, paginateProject
from .forms import ProjectForm, ReviewForm

# Create your views here.
def projects(request):
    # projects = Project.objects.all()    
    projects, search_query = searchProject(request)   # projects as filtered queryset from Project model

    projects, custom_range = paginateProject(request, projects, results=6)   # paginated projects e.g page 1 of 5
    context = {'projects': projects, 'search_query':search_query, 'custom_range':custom_range}    # projects as paginated object (not queryset from Project model)

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    reviewers = [review.owner for review in projectObj.review_set.all()]
    user_has_reviewed = True if (request.user.is_authenticated and request.user.profile in reviewers) else False
    print("Reviewers:", reviewers)
    print("User has reviewed:", user_has_reviewed)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile if request.user.is_authenticated else None
            review.save()
            # Update project vote count
            # projectObj.getVoteCount

            messages.success(request, 'Your review was successfully submitted!')
            return redirect('project', pk=projectObj.id)

    return render(request, 'projects/single-project.html', {'project' : projectObj, 'form':form, 'user_has_reviewed':user_has_reviewed,})

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

            new_tags = request.POST.get('newtags').split(',')  # get new tags from textarea,
            for tag in new_tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag.title())   # avoid duplicate tags by using get_or_create
                project.tags.add(tag_obj)   # add tag to project's tags M2M field

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
            project.save()  # save updated project instance

            # field that doesn't belong to ModelForm need to be manually handled
            # new_tags = request.POST['newtags']    will raise KeyError if 'newtags' not in POST data
            new_tags = request.POST.get('newtags')  
            new_tags = [] if new_tags == '' else new_tags.split(',')  # get new tags from textarea (only if available), convert comma separated string to list

            for tag in new_tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag.title())   # avoid duplicate tags by using get_or_create
                project.tags.add(tag_obj)   # add tag to project's tags M2M field
            
            messages.success(request, 'Project updated successfully.')
            return redirect('my-account')
    return render(request, 'projects/project-form.html', {'form':form, 'project':project})

@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('my-account')
    
    return render(request, 'delete-template.html', {'object':project, 'type':'project'})