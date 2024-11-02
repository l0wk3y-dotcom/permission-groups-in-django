from django.urls import path
from . import views
urlpatterns = [
    path("home",views.home, name="home-page"),
    path('register/', views.register, name='register'),
    path('create-post/', views.create_post, name='create-posts'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('post/ban/<int:pk>/', views.ban_user, name='ban-user'),
]

