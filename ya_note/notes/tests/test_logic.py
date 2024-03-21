from notes.models import Note
from notes.forms import WARNING
from .base_class import TestBaseClass


FORM_DATA = {
    'title': 'slugify me please',
    'text': 'Test Text',
    'slug': 'random-slug-2',
}


class TestNoteCreation(TestBaseClass):

    def test_uniqueness_slug(self):
        FORM_DATA['slug'] = self.note.slug
        response = self.auth_author.post(self.NOTES_ADD_URL, data=FORM_DATA)
        self.assertFormError(response,
                             form='form',
                             field='slug',
                             errors=self.note.slug + WARNING)
        self.assertEqual(Note.objects.count(), self.note_before_count)

    def test_auth_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.auth_author.post(self.NOTES_ADD_URL, data=FORM_DATA)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        note_count = Note.objects.count()
        self.assertEqual(note_count, note_count)
        note = Note.objects.get()
        self.assertEqual(note.title, FORM_DATA.get('title'))
        self.assertEqual(note.text, FORM_DATA.get('text'))
        self.assertEqual(note.slug, FORM_DATA.get('slug'))
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.NOTES_ADD_URL, data=FORM_DATA)
        self.assertEqual(Note.objects.count(), self.note_before_count)

    def test_author_can_delete_note(self):
        response = self.auth_author.delete(self.delete_slug)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), self.note_before_count - 1)

    def test_author_can_edit_note(self):
        response = self.auth_author.post(self.edit_slug, data=FORM_DATA)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, FORM_DATA['text'])
        self.assertEqual(note.slug, FORM_DATA['slug'])
        self.assertEqual(note.title, FORM_DATA['title'])
        self.assertEqual(note.author, self.author)

    def test_slugify_title(self):
        form_data = FORM_DATA.copy()
        form_data.pop('slug')
        self.auth_author.post(self.NOTES_ADD_URL, data=FORM_DATA)
        form_data['slug'] = Note.objects.last().slug
        self.assertEqual(Note.objects.count(), self.note_before_count + 1)
        note = Note.objects.get(slug=FORM_DATA['slug'])
        self.assertEqual(note.slug, FORM_DATA['slug'])
        self.assertEqual(note.title, FORM_DATA['title'])
        self.assertEqual(note.text, FORM_DATA['text'])
        self.assertEqual(note.author, self.author)
