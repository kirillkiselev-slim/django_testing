from notes.models import Note
from notes.forms import WARNING
from .helpers import (
    TestBaseClass,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    DELETE_SLUG_URL,
    EDIT_SLUG_URL
)


FORM_DATA = {
    'title': 'slugify me please',
    'text': 'Test Text',
    'slug': 'random-slug-2',
}


class TestNoteCreation(TestBaseClass):

    def test_uniqueness_slug(self):
        notes_objects_before = list(Note.objects.all())
        FORM_DATA['slug'] = self.note.slug
        response = self.auth_author.post(NOTES_ADD_URL, data=FORM_DATA)
        self.assertFormError(response,
                             form='form',
                             field='slug',
                             errors=self.note.slug + WARNING)
        self.assertEqual(list(Note.objects.all()), notes_objects_before)

    def test_auth_user_can_create_note(self):
        Note.objects.all().delete()
        self.common_setup_and_assertions_create_note(FORM_DATA)

    def test_anonymous_user_cant_create_note(self):
        self.client.post(NOTES_ADD_URL, data=FORM_DATA)
        self.assertEqual(Note.objects.count(), self.note_before_count)

    def test_author_can_delete_note(self):
        response = self.auth_author.delete(DELETE_SLUG_URL)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), self.note_before_count - 1)
        self.assertNotIn(self.note, Note.objects.all())

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
        note = Note.objects.get()
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.text, form_data['text'])
        try:
            self.assertEqual(note.slug, form_data['slug'])
        except KeyError:
            pass
        self.assertEqual(note.author, self.author)
