from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.profile, name='user-profile'),
    path('my-account', views.my_account, name='my-account'),

    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register-user'),

    path('edit-account/', views.edit_account, name='edit-account'),
]
