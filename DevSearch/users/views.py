from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import searchProfiles, paginateProfile
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

# Create your views here.
def profiles(request):
    # profiles = Profile.objects.all()
    profiles, search_query = searchProfiles(request)
    profiles, custom_range = paginateProfile(request, profiles, results=6)  
    context = {'profiles': profiles, 'search_query':search_query, 'custom_range': custom_range}

    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skills.exclude(description__exact="") # only skills with description (skills that don't have description are excluded)
    # exclude() filters out records that match a certain condition — in this case, skills that have an empty description.
    otherSkills = profile.skills.filter(description="") # takes only skills without description

    return render(request, 'users/user-profile.html', {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills})


def loginUser(request):
    page = 'login'    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:    # if verified user
            login(request, user)
            messages.success(request, 'Successfully Logged in.')
            return redirect('my-account')
        else:
            messages.error(request, 'Username or Passowrd incorrect !!!')           

    return render(request, 'users/login_register.html', {'page': page})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')
    

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # to modify user before saving
            user.username = user.username.lower()   # why to lower case? to avoid duplicate usernames with different cases
            user.first_name = user.first_name.title() # capitalize first letter
            user.last_name = user.last_name.title()   # capitalize first letter
            user.email = user.email.lower()
            user.save()
            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('update-account')  # redirect to update account page to fill more details
        else:
            messages.error(request, "An error has occurred during registration.")

    return render(request, 'users/login_register.html', {'page': page, 'form':form})


@login_required(login_url='login')
def my_account(request):
    profile = request.user.profile
    return render(request, 'users/my-account.html', {'profile':profile})


@login_required(login_url='login')
def updateAccount(request):    
    profile = request.user.profile  # request.user.profile gives one to one relationship object of the logged in user.
    form = ProfileForm(instance=profile)
    if request.method =="POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile) # request.FILES contains any uploaded files, such as images or documents.(only works with enctype="multipart/form-data" in form tag)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.name =profile.name.capitalize()
            profile.username = profile.username.lower()
            profile.email = profile.email.lower() if profile.email else None
            form.save()     # request.user.profile gives the existing profile object. so form.save() will update the existing profile. (else profile.save() to update)
            return redirect('my-account')
    return render(request, 'users/profile-form.html', {'form':form})


@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile     # assign owner to skill
            skill.name = skill.name.title()            
            
            # save the new skill instance
            form.save()  # or skill.save()
            
            messages.success(request, 'Skill added successfully.')
            return redirect('my-account')      

    return render(request, 'users/skill-form.html', {'form':form})

@login_required(login_url='login')
def updateSkill(request, pk):
    skill = Skill.objects.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.name = skill.name.capitalize()
            # Save the updated skill instance
            form.save() # or skill.save()

            messages.success(request, 'Skill updated successfully.')
            return redirect('my-account')
    return render(request, 'users/skill-form.html', {'form':form})


@login_required(login_url='login')
def deleteSkill(request, pk):
    skill = Skill.objects.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully.')
        return redirect('my-account')        
    return render(request, 'delete-template.html', {'object':skill, 'type':'skill'})