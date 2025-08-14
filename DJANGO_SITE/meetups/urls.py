from django.urls import path
from . import views

urlpatterns =[
    path('', views.index),  # domain/    
    path('<slug:meetup_slug>', views.meetup_details, name='meetup-detail'),    # doimain/meetups
    path('<slug:meetup_slug>/success', views.confirm_registration, name='confirm-registration'),   
]