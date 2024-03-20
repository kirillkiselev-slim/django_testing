from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

from notes.models import Note
from notes.forms import NoteForm
from .urls_for_tests import NOTES_LIST_URL, NOTES_ADD_URL, edit_slug

User = get_user_model()


class TestBaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.other_user = User.objects.create(username='Reader')
        cls.auth_author, cls.auth_other_user = Client(), Client()
        cls.auth_author.force_login(cls.author)
        cls.auth_other_user.force_login(cls.other_user)
        cls.note = Note.objects.create(
            title='Title_author',
            text='text',
            slug='unique-slug',
            author=cls.author
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


class TestNotesListPage(TestBaseClass):

    def test_note_in_list(self):
        response = self.auth_author.get(NOTES_LIST_URL)
        object_list = response.context['object_list']
        note = Note.objects.get(id=self.note.id)
        self.assertIn(note, object_list)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)

    def test_notes_do_not_mix_for_author(self):
        response = self.auth_author.get(NOTES_LIST_URL)
        object_list = response.context['object_list']
        notes = [notes.slug for notes in object_list]
        notes.pop(0)
        for note in notes:
            self.assertNotIn(note, self.other_user_notes)

    def test_notes_do_not_mix_for_other_user(self):
        response = self.auth_other_user.get(NOTES_LIST_URL)
        object_list = response.context['object_list']
        notes = [notes.slug for notes in object_list]
        for note in notes:
            self.assertNotIn(note, self.author_notes)


class TestDetailNote(TestBaseClass):

    def test_user_sees_edit_and_add_form(self):
        urls = (
            NOTES_ADD_URL,
            edit_slug(self.note.slug)
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.auth_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
