from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth_create = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            author=cls.auth_create,
            text='Тестовый пост',
            id=1
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = Client()
        self.author.force_login(self.auth_create)

    def test_post_index_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        url_status = {
            reverse('posts:index'): HTTPStatus.OK,}
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)       

    def test_post_group_url_exists_at_desired_location(self):
        """Страница /group/ доступна любому пользователю."""
        url_status = {
            reverse(
                'posts:group_list',
                kwargs={'slug': PostURLTests.group.slug}
        ): HTTPStatus.OK,}
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_post_profile_url_exists_at_desired_location(self):
        """Страница /profile/ доступна любому пользователю."""
        url_status = {
            reverse(
                'posts:profile',
                kwargs={'username': PostURLTests.auth_create.username}
        ): HTTPStatus.OK,}
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_post_posts_url_exists_at_desired_location(self):
        """Страница /posts/1/ доступна любому пользователю."""
        url_status = {
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostURLTests.post.id}
        ): HTTPStatus.OK,}
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_post_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        url_status = {
            reverse('posts:post_create'): HTTPStatus.OK,}
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.author.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_post_edit_url_exists_at_desired_location(self):
        """Страница /posts/1/edit доступна автору поста."""
        url_status = {
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostURLTests.post.id}
        ): HTTPStatus.OK,}
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.author.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            self.authorized_client: {
                '/create/': 'posts/create_post.html',
            },
            self.author: {
                '/posts/1/edit/': 'posts/create_post.html',
            },
            self.guest_client: {
                '/': 'posts/index.html',
                '/group/test-slug/': 'posts/group_list.html',
                '/profile/HasNoName/': 'posts/profile.html',
                '/posts/1/': 'posts/post_detail.html',
            }
        }
        for client_type, dict in templates_url_names.items():
            for address, template in dict.items():
                with self.subTest(address=address):
                    response = client_type.get(address)
                    self.assertTemplateUsed(response, template)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_unexisting(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def tearDown(self):
        cache.clear()
