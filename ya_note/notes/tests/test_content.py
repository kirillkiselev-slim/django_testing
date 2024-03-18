from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestNotesListPage(TestCase):
    NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.other_user = User.objects.create(username='Reader')
        cls.auth_author = Client()
        cls.auth_author.force_login(cls.author)
        cls.note = Note.objects.create(
            title='Title_author',
            text='text',
            slug='unique-slug',
            author=cls.author
        )

        author_notes = [
            Note(
                title=f'Title_author{index}',
                text='text_author',
                slug=f'{int(index)}_unique-slug-author',
                author=cls.author
            ) for index in range(1, 11)
        ]
        Note.objects.bulk_create(author_notes)

        other_user_notes = [
            Note(
                title=f'Title_other_user{index}',
                text='text_other_user',
                slug=f'{int(index)}_unique-slug-other-user',
                author=cls.other_user
            ) for index in range(1, 11)
        ]
        Note.objects.bulk_create(other_user_notes)

    def test_note_in_list(self):
        response = self.auth_author.get(self.NOTES_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_notes_do_not_mix_for_users(self):
        self.client.force_login(self.other_user)
        response_author = self.auth_author.get(self.NOTES_URL)
        response_other_user = self.client.get(self.NOTES_URL)
        object_list_author = response_author.context['object_list']
        object_list_other_user = response_other_user.context['object_list']
        all_notes_author = sorted([notes.slug for notes in object_list_author])
        all_notes_other_user = sorted([notes.slug
                                       for notes in object_list_other_user])
        for note_author, note_other_user in zip(all_notes_author,
                                                all_notes_other_user):
            self.assertNotEqual(note_author, note_other_user)


class TestDetailNote(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.note = Note.objects.create(
            title='Title_author',
            text='text_author',
            slug='unique-slug',
            author=cls.author
        )

        cls.auth_author = Client()
        cls.auth_author.force_login(cls.author)

    def test_user_sees_edit_and_add_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.auth_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
