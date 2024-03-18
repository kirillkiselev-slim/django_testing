from http import HTTPStatus
from pytest_django.asserts import assertFormError
from news.forms import WARNING, BAD_WORDS
from django.urls import reverse
from news.models import Comment
import pytest


@pytest.mark.django_db
def test_anonymous_user_cannot_leave_comment(client, form_data, pk_for_args):
    url = reverse('news:detail', args=pk_for_args)
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_authorized_user_can_leave_comment(author_client,
                                           form_data, pk_for_args):
    url = reverse('news:detail', args=pk_for_args)
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    comments = Comment.objects.get()
    assert comments.news == form_data['news']
    assert comments.author == form_data['author']
    assert comments.text == form_data['text']


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_bad_words(author_client, bad_word, pk_for_args):
    url = reverse('news:detail', args=pk_for_args)
    bad_word_data = {'text': f'comment with the bad word "{bad_word}"'}
    response = author_client.post(url, data=bad_word_data)
    assertFormError(response, 'form', 'text',
                    errors=WARNING)


def test_author_can_edit_comment(author_client, form_data_edit_comment,
                                 comment):
    url = reverse('news:edit', args=(comment.id,))
    author_client.post(url, data=form_data_edit_comment)
    comment.refresh_from_db()
    assert comment.news == form_data_edit_comment['news']
    assert comment.text == form_data_edit_comment['text']
    assert comment.author == form_data_edit_comment['author']


def test_other_user_cant_edit_comment(not_author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Comment.objects.get(id=comment.id)
    assert comment.author == note_from_db.author
    assert comment.text == note_from_db.text
    assert comment.news == note_from_db.news


def test_author_can_delete_comment(author_client, form_data, pk_for_comment):
    url = reverse('news:delete', args=pk_for_comment)
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_note(not_author_client,
                                     form_data, pk_for_comment):
    url = reverse('news:delete', args=pk_for_comment)
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
