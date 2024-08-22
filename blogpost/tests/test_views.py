from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blogpost.models import Post
from blogpost.views import PostListView, PostDetailView, PostCreateView

# blogpost/tests.py

class BlogpostViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content',
            status='published',
        )

    def test_post_list_view(self):
        url = reverse('blogpost:post_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpost/post_list.html')
        self.assertContains(response, self.post.title)
        self.assertQuerysetEqual(
            response.context['posts'],
            Post.objects.filter(status='published').order_by('-published_at')
        )

    def test_post_detail_view(self):
        url = reverse('blogpost:post_detail', args=[self.post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpost/post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertEqual(response.context['post'], self.post)

    def test_post_create_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('blogpost:post_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpost/post_form.html')

        # Test form submission
        post_data = {
            'title': 'Another Test Post',
            'slug': 'another-test-post',
            'content': 'Content for another test post',
            'status': 'published',
        }
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)  # Redirect after post creation
        new_post = Post.objects.get(slug='another-test-post')
        self.assertEqual(new_post.title, 'Another Test Post')
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.content, 'Content for another test post')
        self.assertEqual(new_post.status, 'published')

    def test_post_create_view_redirect_for_anonymous(self):
        url = reverse('blogpost:post_create')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={url}')

