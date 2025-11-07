from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Profile, Skill

def searchProfiles(request):
    search_query = request.GET.get('search_query')
    search_query = search_query if search_query else ''
    
    skills = Skill.objects.filter(name__icontains=search_query)


    profiles = Profile.objects.filter(
        Q(first_name__icontains = search_query) |
        Q(last_name__icontains = search_query) |
        Q(short_intro__icontains = search_query) |        
        Q(skills__in = skills)
    ).distinct()   # profiles as a queryset from Profile model

    return profiles, search_query    


def paginateProfile(request, profiles, results):    
    page = request.GET.get('page')
    page = page if page else 1 
    
    paginator = Paginator(profiles, results)
    
    # convert profiles queryset to paginated object e.g. page 1 of 3
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1    # If page is not an integer, deliver the first page.
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # If page is out of range, deliver last page of results.
        profiles = paginator.page(page)


    leftIndex = int(page) - 2
    rightIndex = int(page) + 3

    if leftIndex < 1:
        leftIndex = 1   
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)

    return profiles, custom_range