from django.shortcuts import render
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
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:    # if verified user
            login(request, user)
            messages.success(request, 'Successfully Logged in.')
            return render(request, 'users/my-account.html')
        else:
            messages.error(request, 'Username or Passowrd incorrect !!!')   
        

    return render(request, 'users/login_register.html', {'page': page})

def logoutUser(request):
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