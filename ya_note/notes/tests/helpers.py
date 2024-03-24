from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from notes.models import Note

SLUG = 'random-slug-1'

NOTES_HOME_URL = reverse('notes:home')
NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTES_SUCCESS_URL = reverse('notes:success')
SIGN_UP_URL = reverse('users:signup')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
REDIRECT_URL = f'{LOGIN_URL}?next='
DETAIL_SLUG_URL = reverse('notes:detail', args=(SLUG,))
EDIT_SLUG_URL = reverse('notes:edit', args=(SLUG,))
DELETE_SLUG_URL = reverse('notes:delete', args=(SLUG,))


class TestBaseClass(TestCase):
    CLIENT = Client()
    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.author = cls.User.objects.create(username='Author')
        cls.other_user = cls.User.objects.create(username='Reader')
        cls.auth_author, cls.auth_other_user = Client(), Client()
        cls.auth_author.force_login(cls.author)
        cls.auth_other_user.force_login(cls.other_user)
        cls.note = Note.objects.create(
            title='Title_0',
            text='text',
            slug=SLUG,
            author=cls.author
        )
        cls.other_user_note = Note.objects.create(
            title='Title_0-other-user',
            text='text-other-user',
            slug='other-usr-random-slug-1',
            author=cls.other_user
        )

        cls.author_notes = [
            Note(
                title=f'Title_author{index}',
                text='text_author',
                slug=f'{int(index)}_unique-slug-author',
                author=cls.author
            ) for index in range(1, 11)
        ]
        Note.objects.bulk_create(cls.author_notes)

        cls.other_user_notes = [
            Note(
                title=f'Title_other_user{index}',
                text='text_other_user',
                slug=f'{int(index)}_unique-slug-other-user',
                author=cls.other_user
            ) for index in range(1, 11)
        ]
        Note.objects.bulk_create(cls.other_user_notes)

        cls.form_data_not_unique = {
            'title': 'slug which holds no purpose',
            'text': 'Some random text written here',
            'slug': 'test-not-unique-slug',
        }
        cls.note_before_count = Note.objects.count()
