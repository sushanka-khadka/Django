from django.shortcuts import render
from .models import Profile
from .utils import searchProfiles, paginateProfile

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