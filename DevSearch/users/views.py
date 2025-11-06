from django.shortcuts import render, redirect
from .models import Profile
from .utils import searchProfiles, paginateProfile

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def loginUser(request):
    page = 'login'    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:    # if verified user
            login(request, user)
            messages.success(request, 'Successfully Logged in.')
            return render(request, 'users/my-account.html')
        else:
            messages.error(request, 'Username or Passowrd incorrect !!!')           

    return render(request, 'users/login_register.html', {'page': page})

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')
    
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
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
            user.save()
            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "An error has occurred during registration.")

    return render(request, 'users/login_register.html', {'page': page, 'form':form})


def edit_account(request):
    pass



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

def my_account(request):
    profile = request.user.profile
    return render(request, 'users/my-account.html', {'profile':profile})