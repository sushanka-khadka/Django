from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

monthly_challenges= {
    'january': 'Eat no meat for the entire month!',
    'february': 'Walk 5K every day!',
    'march': 'Learn Django for 30 days!',
    'april': 'Practice coding for 1 hour every day!',
    'may': 'Read 2 books this month!',
    'june': 'Run 100 miles this month!',
    'july': 'Drink 2 liters of water every day!',
    'august': 'Meditate for 10 minutes every day!',
    'september': 'Write a blog post every week!',
    'october': 'Complete a coding challenge every day!',
    'november': '',
    'december': None
}


def index(request):
    months= monthly_challenges.keys()
    
    return render(request, 'challenges/index.html', {
        'months': months,
    })

from  django.http import Http404
def monthly_challenge(request, month):
    try: 
        challenge_text= monthly_challenges[month]
    except:
        raise Http404   # return 404 page if avilable 
        # return render_to_string("page not found") 
        # return HttpResponse('Page Not Found')
        # return render(request, '404.html')
    
    return render(request, 'challenges/challenge.html', {
        'month':month,
        'challenge': challenge_text
    })

from django.http import HttpResponseNotFound

def monthly_challenge_by_number(request, month):
    months= list(monthly_challenges.keys())
    if month > len(months):
        return HttpResponseNotFound('<h1>Invalid Month</h1>')

    redirected_month = months[month - 1]
    # redirected_path = '/challenges/' +  redirected_month    # static path can cause error if main url is changed
    redirected_path = reverse('month-challenge', args=[redirected_month])
    return HttpResponseRedirect(redirected_path)