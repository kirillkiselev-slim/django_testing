from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from notes.models import Note

SLUG = 'random-slug-1'
FORM_DATA_SLUG = 'random-slug-2'
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
USER = get_user_model()
FORM_DATA = {
    'title': 'slugify me please',
    'text': 'Test Text',
    'slug': 'random-slug-2',
}


class TestBaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = USER.objects.create(username='Author')
        cls.other_user = USER.objects.create(username='Reader')
        cls.auth_author, cls.auth_other_user = Client(), Client()
        cls.auth_author.force_login(cls.author)
        cls.auth_other_user.force_login(cls.other_user)
        cls.note = Note.objects.create(
            title='Title_0',
            text='text',
            slug=SLUG,
            author=cls.author
        )

        cls.note_before_count = Note.objects.count()
