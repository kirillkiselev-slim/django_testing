from notes.forms import NoteForm
from .helpers import (
    TestBaseClass,
    NOTES_LIST_URL,
    EDIT_SLUG_URL,
    NOTES_ADD_URL
)


class TestNotesListPage(TestBaseClass):

    def test_note_in_list(self):
        response = self.auth_author.get(NOTES_LIST_URL)
        notes_queryset = response.context['object_list']
        self.assertIn(self.note, notes_queryset)
        note = notes_queryset.get(pk=self.note.pk)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)

    def test_notes_do_not_mix_for_author(self):
        response = self.auth_other_user.get(NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_user_sees_edit_and_add_form(self):
        urls = (
            NOTES_ADD_URL,
            EDIT_SLUG_URL
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
