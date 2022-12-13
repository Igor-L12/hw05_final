import shutil
import tempfile
from itertools import islice

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Group, Post, Follow

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.auth_create = User.objects.create_user(username='auth')
        cls.user = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.auth_create,
            id=1,
            group=cls.group,
            image=uploaded
        )
        cls.comments = Comment.objects.create(
            author=cls.user,
            text='Тестовый коммент',
            post=cls.post
        )

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовые медиа."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
    
    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = Client()
        self.author.force_login(self.auth_create)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            self.authorized_client: {
                reverse('posts:post_create'): 'posts/create_post.html',
            },
            self.author: {
                reverse(
                    'posts:post_edit',
                    kwargs={'post_id': self.post.id}): 'posts/create_post.html'
            },
            self.guest_client: {
                reverse('posts:index'): 'posts/index.html',
                reverse(
                    'posts:group_list',
                    kwargs={'slug': self.group.slug}): 'posts/group_list.html',
                reverse(
                    'posts:profile',
                    kwargs={'username': self.user}): 'posts/profile.html',
                reverse(
                    'posts:post_detail',
                    kwargs={'post_id': self.post.id}): 'posts/post_detail.html'
            },
        }
        for client_type, dict in templates_page_names.items():
            for address, template in dict.items():
                with self.subTest(address=address):
                    response = client_type.get(address)
                    self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_group_0, 'Тестовый заголовок')
        self.assertEqual(post_image_0, 'posts/small.gif')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list', kwargs={
                    'slug': self.group.slug}))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        group_title_test_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(group_title_test_0, 'Тестовый заголовок')
        self.assertEqual(post_image_0, 'posts/small.gif')

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.author.get(
            reverse(
                'posts:profile', kwargs={
                    'username': PostViewTests.auth_create.username}))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        author_test_0 = first_object.author
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(author_test_0, PostViewTests.auth_create)
        self.assertEqual(post_image_0, 'posts/small.gif')

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:post_detail',
                    kwargs={
                        'post_id': PostViewTests.post.id,
                    })))
        first_object = response.context['post']
        post_text_0 = first_object.text
        post_image_0 = first_object.image
        post_comment = PostViewTests.comments.text
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_image_0, 'posts/small.gif')
        self.assertEqual(post_comment, 'Тестовый коммент')

    def test_post_create_pages_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_fields = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_fields, expected)

    def test_post_edit_pages_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = (self.author.
                    get(reverse(
                        'posts:post_edit',
                        kwargs={'post_id': PostViewTests.post.id})))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_paginator_correct_context(self):
        """Шаблон index,
        group_list и profile сформированы с корректным Paginator."""
        batch_size = 100
        paginator_obj = (
            Post(
                author=PostViewTests.auth_create,
                text='Тестовый пост ' + str(i),
                group=PostViewTests.group
            )
            for i in range(12))
        while True:
            batch = list(islice(paginator_obj, batch_size))
            if not batch:
                break
            Post.objects.bulk_create(batch, batch_size)
        paginator_data = {
            'index': reverse('posts:index'),
            'group': reverse(
                'posts:group_list',
                kwargs={'slug': PostViewTests.group.slug}),
            'profile': reverse(
                'posts:profile',
                kwargs={'username': PostViewTests.auth_create.username})
        }
        for paginator_place, paginator_page in paginator_data.items():
            with self.subTest(paginator_place=paginator_place):
                response_page_1 = self.authorized_client.get(paginator_page)
                response_page_2 = self.authorized_client.get(
                    paginator_page + '?page=2')
                self.assertEqual(len(response_page_1.context['page_obj']), 10)
                self.assertEqual(len(response_page_2.context['page_obj']), 3)

    def text_index_cache(self):
        """Тестирование кэша страницы index"""
        post = Post.objects.create(
            author=PostViewTests.auth_create,
            text='Тестовый пост',
            group=PostViewTests.group
        )
        response_1 = self.authorized_client.get(
            reverse('posts:index')
        )
        response_1_content = response_1.content
        post.delete()
        response_2 = self.authorized_client.get(
            reverse('posts:index')
        )
        response_content_2 = response_2.content
        self.assertEqual(response_1_content, response_content_2)
        cache.clear()
        response_3 = self.authorized_client.get(
            reverse('posts:index')
        )
        response_content_3 = response_3.content
        self.assertNotEqual(response_content_2, response_content_3)
    
    def tearDown(self):
        cache.clear()

    def test_follow(self):
        """Тестирование подписки на автора."""
        count_follow = Follow.objects.count()
        new_author = User.objects.create(username='User')
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': new_author.username}
            )
        )
        follow = Follow.objects.last()
        self.assertEqual(Follow.objects.count(), count_follow + 1)
        self.assertEqual(follow.author, new_author)
        self.assertEqual(follow.user, PostViewTests.user)

    def test_unfollow(self):
        """Тестирование отписки от автора."""
        count_follow = Follow.objects.count()
        new_author = User.objects.create(username='User')
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': new_author.username}
            )
        )
        self.assertEqual(Follow.objects.count(), count_follow + 1)
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': new_author.username}
            )
        )
        self.assertEqual(Follow.objects.count(), count_follow)

    def test_following_posts(self):
        """Тестирование появления поста автора в ленте подписчика."""
        new_user = User.objects.create(username='User')
        authorized_client = Client()
        authorized_client.force_login(new_user)
        authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostViewTests.user.username}
            )
        )
        response_follow = (
            self.authorized_client.get(
                reverse(
                    'posts:follow_index'
                    )))
        first_object = response_follow.context
        self.assertNotEqual(len(first_object['page_obj']), 1)

    def test_unfollowing_posts(self):
        """Тестирование отсутствия поста автора у нового пользователя."""
        new_user = User.objects.create(username='User')
        authorized_client = Client()
        authorized_client.force_login(new_user)
        response_unfollow = authorized_client.get(
            reverse('posts:follow_index')
        )
        context_unfollow = response_unfollow.context
        self.assertEqual(len(context_unfollow['page_obj']), 0)