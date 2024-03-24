from http import HTTPStatus

from notes.models import Note
from notes.forms import WARNING
from pytils.translit import slugify

from .helpers import (
    TestBaseClass,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    DELETE_SLUG_URL,
    EDIT_SLUG_URL,
    FORM_DATA,
    FORM_DATA_SLUG
)


class TestNoteCreation(TestBaseClass):

    def test_uniqueness_slug(self):
        notes = Note.objects.order_by('title')
        FORM_DATA['slug'] = self.note.slug
        response = self.auth_author.post(NOTES_ADD_URL, data=FORM_DATA)
        self.assertFormError(response,
                             form='form',
                             field='slug',
                             errors=self.note.slug + WARNING)
        self.assertQuerysetEqual(Note.objects.order_by('title'), notes)

    def test_auth_user_can_create_note(self):
        self.common_setup_and_assertions_create_note(FORM_DATA)

    def test_anonymous_user_cant_create_note(self):
        notes = Note.objects.order_by('title')
        self.client.post(NOTES_ADD_URL, data=FORM_DATA)
        self.assertQuerysetEqual(Note.objects.order_by('title'), notes)

    def test_author_can_delete_note(self):
        response = self.auth_author.delete(DELETE_SLUG_URL)
        note_exists = Note.objects.filter(pk=self.note.pk).exists()
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), self.note_before_count - 1)
        self.assertFalse(note_exists)

    def test_other_user_cant_delete_note(self):
        response = self.auth_other_user.post(DELETE_SLUG_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), self.note_before_count)

    def test_author_can_edit_note(self):
        response = self.auth_author.post(EDIT_SLUG_URL, data=FORM_DATA)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, FORM_DATA['text'])
        self.assertEqual(note.slug, FORM_DATA['slug'])
        self.assertEqual(note.title, FORM_DATA['title'])
        self.assertEqual(note.author, self.note.author)

    def test_slugify_title(self):
        form_data = FORM_DATA.copy()
        form_data.pop('slug')
        self.common_setup_and_assertions_create_note(form_data)

    def common_setup_and_assertions_create_note(self, form_data):
        Note.objects.all().delete()
        response = self.auth_author.post(NOTES_ADD_URL, data=form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        note_title = form_data['title']
        self.assertEqual(note.title, note_title)
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.author, self.author)
        if note.slug != FORM_DATA_SLUG:
            self.assertEqual(note.slug, slugify(note_title))
        else:
            self.assertEqual(note.slug, form_data['slug'])
