from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='reader')
        cls.notes = Note.objects.create(title='Заголовок', text='Текст',
                                        author=cls.author,
                                        slug='some-random-slug')

    def test_availability_for_notes_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.notes.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_pages_availability_for_anonymous_client(self):
        urls = (
            ('notes:home', None),
            ('notes:list', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
            ('notes:add', None),
            ('notes:success', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                if name not in ('notes:list', 'notes:add', 'notes:success'):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

                self.client.force_login(self.author)
                response = self.client.get(url)

                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:edit', (self.notes.slug,)),
            ('notes:delete', (self.notes.slug,)),
            ('notes:detail', (self.notes.slug,)),
            ('notes:list', None),
            ('notes:add', None),
            ('notes:success', None)
        )
        for name, args in urls:
            url = reverse(name, args=args)
            with self.subTest(name=name):
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
