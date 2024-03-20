from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note
from notes.forms import WARNING
from .urls_for_tests import *

User = get_user_model()

TITLE = 'slugify me please'

TEST_SLUG = 'test-not-unique-slug'

FORM_DATE_UNIQUE = {
    'title': TITLE,
    'text': 'Test Text',
    'slug': 'unique-slug',
}


class TestBaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('user')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.note = Note.objects.create(slug='test-not-unique-slug',
                                       author=cls.user)

        cls.form_data_not_unique = {
            'slug': TEST_SLUG,
        }


class TestNoteCreation(TestBaseClass):

    def test_uniqueness_slug(self):
        response = self.auth_user.post(NOTES_ADD_URL,
                                       data=self.form_data_not_unique)
        self.assertFormError(response,
                             form='form',
                             field='slug',
                             errors=TEST_SLUG + WARNING)
        self.assertEqual(Note.objects.count(), 1)

    def test_auth_user_can_create_note(self):
        response = self.auth_user.post(NOTES_ADD_URL, data=FORM_DATE_UNIQUE)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 2)
        note = Note.objects.last()
        self.assertEqual(note.title, FORM_DATE_UNIQUE.get('title'))
        self.assertEqual(note.text, FORM_DATE_UNIQUE.get('text'))
        self.assertEqual(note.slug, FORM_DATE_UNIQUE.get('slug'))

    def test_anonymous_user_cant_create_note(self):
        self.client.post(NOTES_ADD_URL, data=FORM_DATE_UNIQUE)
        self.assertEqual(Note.objects.count(), 1)


class TestNoteEditDelete(TestBaseClass):

    def test_author_can_delete_note(self):
        response = self.auth_user.delete(delete_slug(self.note.slug))
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 0)

    def test_author_can_edit_note(self):
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        response = self.auth_user.post(
            edit_slug(self.note.slug), data=FORM_DATE_UNIQUE)

        self.assertRedirects(response, NOTES_SUCCESS_URL)
        note_updated = Note.objects.get(pk=note.pk)
        self.assertEqual(note_updated.text, FORM_DATE_UNIQUE['text'])
        self.assertEqual(note_updated.slug, FORM_DATE_UNIQUE['slug'])
        self.assertEqual(note_updated.title, FORM_DATE_UNIQUE['title'])


class TestSlugifyTitle(TestBaseClass):

    def test_slugify_title(self):
        form_data = FORM_DATE_UNIQUE.copy()
        form_data.pop('slug')
        self.auth_user.post(NOTES_ADD_URL, data=FORM_DATE_UNIQUE)
        form_data['slug'] = Note.objects.last().slug
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.last()
        self.assertEqual(new_note.slug, form_data['slug'])
        self.assertEqual(new_note.title, FORM_DATE_UNIQUE['title'])
        self.assertEqual(new_note.text, FORM_DATE_UNIQUE['text'])
