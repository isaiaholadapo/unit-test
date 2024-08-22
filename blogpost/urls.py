from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

app_name = 'blogpost'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
