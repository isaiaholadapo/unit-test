from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .form import PostForm
from .models import Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogpost/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published':
            form.instance.publish()
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'blogpost/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_at']
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-published_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogpost/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')


