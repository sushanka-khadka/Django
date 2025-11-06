from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.profile, name='user-profile'),
    path('my-account', views.my_account, name='my-account'),

    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register-user'),

    path('update-account/', views.updateAccount, name='update-account'),
    path('create-skill/', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>', views.updateSkill, name='update-skill'),    
    path('delete-skill/<str:pk>', views.deleteSkill, name='delete-skill'),    
]
