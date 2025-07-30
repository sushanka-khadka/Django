from django.urls import path
from . import views

urlpatterns =[
    path('', views.StartingPageView.as_view(), name='starting-page'),  # /
    path('posts/', views.AllPostsView.as_view(), name='posts-page'),  # posts/
    path('posts/<slug:slug>/', views.SinglePostView.as_view(), name='post-detail-page'),   # posts/my-blog-post/
    path('read-later', views.ReadLaterView.as_view(), name='read-later'),  # read-later/
]

# slug is a variable part of the URL that can be used to identify a specific post
