from pytest_django.asserts import assertFormError
from django.urls import reverse
import pytest
from http import HTTPStatus

from news.models import Comment
from news.forms import WARNING, BAD_WORDS

pytestmark = pytest.mark.django_db

BAD_WORD_DATA = {'text': f'comment with the bad word "{BAD_WORDS[0]}"'}


def test_anonymous_user_cannot_post_comment(client, form_data, news):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_authorized_user_can_leave_comment(author_client,
                                           form_data, news):
    url = reverse('news:detail', args=(news.id,))
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    comments = Comment.objects.get()
    assert comments.text == form_data['text']


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_bad_words(author_client, bad_word, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=BAD_WORD_DATA)
    assertFormError(response, 'form', 'text',
                    errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, form_data_edit_comment,
                                 comment):
    comment = Comment.objects.get(pk=comment.pk)
    url = reverse('news:edit', args=(comment.id,))
    author_client.post(url, data=form_data_edit_comment)
    updated_comment = Comment.objects.get(pk=comment.pk)

    assert comment.news == updated_comment.news
    assert comment.text != updated_comment.text
    assert comment.author == updated_comment.author


def test_other_user_cant_edit_comment(not_author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_updated = Comment.objects.get(id=comment.id)
    assert comment.author == comment_updated.author
    assert comment.text == comment_updated.text
    assert comment.news == comment_updated.news


def test_author_can_delete_comment(author_client, form_data, comment):
    url = reverse('news:delete', args=(comment.id,))
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_note(not_author_client,
                                     form_data, comment):
    assert Comment.objects.count() == 1
    url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
