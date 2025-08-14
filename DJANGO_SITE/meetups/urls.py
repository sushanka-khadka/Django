from django.urls import path
from . import views

urlpatterns =[
    path('', views.index),  # domain/
    path('meetups/success', views.confirm_registration, name='confirm-registration'),
    path('meetups/<slug:meetup_slug>', views.meetup_details, name='meetup-detail'),    # doimain/meetups
]