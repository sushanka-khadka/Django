from . import views
from django.urls import path
from django.views.generic import RedirectView


urlpatterns =[
    path('', RedirectView.as_view(url='/challenges', permanent=True)),
    path('challenges/', views.index, name='index'),
    path('challenges/<int:month>', views.monthly_challenge_by_number),      # this shoould be before <str:month> else even int will be taken as str
    path('challenges/<str:month>', views.monthly_challenge, name='month-challenge')
]