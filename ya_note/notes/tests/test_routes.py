from http import HTTPStatus

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

from notes.models import Note
from .urls_for_tests import (
    NOTES_ADD_URL,
    NOTES_HOME_URL,
    NOTES_LIST_URL,
    NOTES_SUCCESS_URL,
    detail_slug,
    edit_slug,
    delete_slug,
    SIGN_UP_URL,
    LOGIN_URL,
    LOGOUT_URL,
)

User = get_user_model()

CLIENT = Client()

OK_STATUS = HTTPStatus.OK

NOT_FOUND_STATUS = HTTPStatus.NOT_FOUND


class TestBaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='reader')
        cls.auth_author, cls.auth_reader = Client(), Client()
        cls.auth_author.force_login(cls.author)
        cls.auth_reader.force_login(cls.reader)

        cls.note = Note.objects.create(title='Заголовок', text='Текст',
                                       author=cls.author,
                                       slug='some-random-slug')


class TestRoutes(TestBaseClass):
    def test_availability_for_pages(self):
        parametrized_scenarios = (
            (detail_slug(self.note.slug), self.auth_author, OK_STATUS),
            (detail_slug(self.note.slug), self.auth_reader, NOT_FOUND_STATUS),
            (edit_slug(self.note.slug), self.auth_author, OK_STATUS),
            (edit_slug(self.note.slug), self.auth_reader, NOT_FOUND_STATUS),
            (delete_slug(self.note.slug), self.auth_author, OK_STATUS),
            (delete_slug(self.note.slug), self.auth_reader, NOT_FOUND_STATUS),
            (NOTES_LIST_URL, self.auth_author, OK_STATUS),
            (NOTES_ADD_URL, self.auth_author, OK_STATUS),
            (NOTES_SUCCESS_URL, self.auth_author, OK_STATUS),
            (NOTES_HOME_URL, CLIENT, OK_STATUS),
            (LOGIN_URL, CLIENT, OK_STATUS),
            (LOGOUT_URL, CLIENT, OK_STATUS),
            (SIGN_UP_URL, CLIENT, OK_STATUS),
        )

        for url, user, status in parametrized_scenarios:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        parametrized_scenarios = (
            (edit_slug(self.note.slug), CLIENT),
            (edit_slug(self.note.slug), CLIENT),
            (edit_slug(self.note.slug), CLIENT),
            (NOTES_LIST_URL, CLIENT),
            (NOTES_ADD_URL, CLIENT),
            (NOTES_SUCCESS_URL, CLIENT)
        )

        for url, user in parametrized_scenarios:
            with self.subTest(url=url, user=user):
                redirect_url = f'{LOGIN_URL}?next={url}'
                self.assertRedirects(user.get(url), redirect_url)
