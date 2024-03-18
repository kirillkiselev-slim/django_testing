from pytils.translit import slugify

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestNoteUniqueness(TestCase):
    TEST_SLUG = 'test-not-unique-slug'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('user')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.note = Note.objects.create(slug='test-not-unique-slug',
                                       author=cls.user)
        cls.add_url = reverse('notes:add')

        cls.form_data_not_unique = {
            'slug': cls.TEST_SLUG,
        }

    def test_uniqueness_slug(self):
        response = self.auth_user.post(self.add_url,
                                       data=self.form_data_not_unique)
        self.assertFormError(response,
                             form='form',
                             field='slug',
                             errors=self.TEST_SLUG + WARNING)


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('user')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.add_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')

        cls.form_data = {
            'title': 'Test Title',
            'text': 'Test Text',
            'slug': 'unique',
            'author': cls.user
        }

    def test_auth_user_can_create_note(self):
        response = self.auth_user.post(self.add_url,
                                       data=self.form_data)
        self.assertRedirects(response, self.success_url)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data.get('title'))
        self.assertEqual(note.author, self.form_data.get('author'))
        self.assertEqual(note.text, self.form_data.get('text'))
        self.assertEqual(note.slug, self.form_data.get('slug'))

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.add_url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)


class TestNoteEditDelete(TestCase):
    NOTES_TEXT = 'nice one'
    NEW_NOTE_TEXT = 'great one'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.success_url = reverse('notes:success')
        cls.note = Note.objects.create(slug='test-slug', author=cls.author,
                                       text=cls.NOTES_TEXT)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

        cls.form_data = {'title': 'title',
                         'text': cls.NEW_NOTE_TEXT,
                         'slug': 'test-slug-edit'}

    def test_author_can_delete_note(self):
        response = self.auth_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_author_can_edit_note(self):
        response = self.auth_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)


class TestSlugifyTitle(TestCase):
    TITLE = 'slugify me please'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='User')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.add_url = reverse('notes:add')

        cls.form_data = {'title': cls.TITLE,
                         'text': 'text'
                         }

    def test_slugify_title(self):
        self.auth_client.post(self.add_url, data=self.form_data)
        note = Note.objects.get()
        self.assertEqual(note.slug, slugify(self.TITLE))
