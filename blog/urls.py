from django.urls import path

from blog.apps import BlogConfig
from blog.views import *

app_name = BlogConfig.name

urlpatterns = [
    path('new_post/', PostCreateView.as_view(), name='new_post'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('edit_post/<int:pk>', PostUpdateView.as_view(), name='edit'),
    path('delete_post/<int:pk>', PostDeleteView.as_view(), name='delete'),
]
