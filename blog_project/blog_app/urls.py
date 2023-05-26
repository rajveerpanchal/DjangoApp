from django.urls import path
from .views import create_post, edit_post, get_all_posts

urlpatterns = [
    path('posts/', create_post, name='create_post'),
    path('posts/<int:post_id>/', edit_post, name='edit_post'),
    path('posts/', get_all_posts, name='get_all_posts'),
]
