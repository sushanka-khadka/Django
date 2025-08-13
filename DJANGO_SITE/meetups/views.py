from django.shortcuts import render

# Create your views here.

def index(request):
    meetups = [
        {
            'title': 'A First Meetup',
            'location': 'Kathmandu',
            'slug': 'a-first-meetup'
        },
        {
            'title': 'A Second Meetup',
            'location': 'Lalitpur',
            'slug': 'a-second-meetup'
        },
    ]

    return render(request, 'meetups/index.html', {
        'meetups': meetups
    })


def meetup_details(request, meetup_slug):
    selected_meetup= {
            'title': 'A Second Meetup',
            'description': 'This is the biggest meetup event ongoing.',            
        }
    return render(request, 'meetups/meetup-detail.html', {
        'meetup_title': selected_meetup['title'],
        'meetup_description': selected_meetup['description']
    });