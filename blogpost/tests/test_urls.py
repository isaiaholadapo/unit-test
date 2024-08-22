from django.test import TestCase
from django.urls import reverse, resolve
from blogpost.views import PostListView, PostDetailView, PostCreateView
from blogpost.models import Post
from django.contrib.auth.models import User


class BlogpostURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content',
            status='published',
        )

    def test_post_list_url(self):
        url = reverse('blogpost:post_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpost/post_list.html')
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_post_detail_url(self):
        url = reverse('blogpost:post_detail', args=[self.post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpost/post_detail.html')
        self.assertEqual(resolve(url).func.view_class, PostDetailView)

    def test_post_create_url(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('blogpost:post_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogpost/post_form.html')
        self.assertEqual(resolve(url).func.view_class, PostCreateView)

    def test_post_create_url_redirect_for_anonymous(self):
        url = reverse('blogpost:post_create')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={url}')
