from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=(
            ('draft', 'Draft'),
            ('published', 'Published'),
        ),
        default='draft',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def publish(self):
        self.published_at = timezone.now()
        self.status = 'published'
        self.save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blogpost:post_detail', args=[self.slug])
