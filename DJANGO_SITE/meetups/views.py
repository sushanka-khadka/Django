from django.shortcuts import render, redirect
from .models import Meetup, Participant
from .forms import RegistrationForm
# Create your views here.

def index(request):
    meetups= Meetup.objects.all()
    return render(request, 'meetups/index.html', {
        'meetups': meetups
    })


def meetup_details(request, meetup_slug):
    try:
        selected_meetup= Meetup.objects.get(slug=meetup_slug)
        if request.method == 'GET':
            registration_form = RegistrationForm()
        else:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data['email']
                participant, was_created= Participant.objects.get_or_create(email= user_email)
                # participant =registration_form.save()   # saving form to model Participant
                selected_meetup.participants.add(participant)   # adding to many to many field                
                return redirect('confirm-registration')            
        return render(request, 'meetups/meetup-detail.html', {
            'meetup_found': True,
            'meetup_item': selected_meetup,
            'form': registration_form
        });
    except Exception as ex:
        print(ex)
        return render(request, 'meetups/meetup-detail.html', {
            'meetup_found': False
        });

def confirm_registration(request):
    return render(request, 'meetups/registration-success.html')