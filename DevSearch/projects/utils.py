from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Project, Tag

def searchProject(request):
    search_query = request.GET.get('search_query')
    search_query = search_query if search_query else ''

    tags = Tag.objects.filter(name__icontains=search_query)
    
    projects = Project.objects.filter(
        Q(title__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(owner__name__icontains = search_query) |
        Q(tags__in = tags)
    ).distinct()   # # projects as a queryset from Project model

    return projects, search_query    


def paginateProject(request, projects, results):    
    page = request.GET.get('page')
    page = page if page else 1 
    
    paginator = Paginator(projects, results)
    
    # convert projects queryset to paginated object e.g. page 1 of 3
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1    # If page is not an integer, deliver the first page.
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # If page is out of range, deliver last page of results.
        projects = paginator.page(page)


    leftIndex = int(page) - 2
    rightIndex = int(page) + 3

    if leftIndex < 1:
        leftIndex = 1   
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)

    return projects, custom_range