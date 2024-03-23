from http import HTTPStatus

from pytest_django.asserts import assertFormError
import pytest

from news.models import Comment
from news.forms import WARNING, BAD_WORDS

pytestmark = pytest.mark.django_db

BAD_WORD_DATA = [{'text': f'comment with the bad word "{word}"'}
                 for word in BAD_WORDS]

FORM_DATA = {
    'text': 'not a random comment'
}

FORM_DATA_EDIT_COMMENT = {
    'text': 'edit not a random comment'
}


def test_anonymous_user_cannot_post_comment(client, news_detail):
    client.post(news_detail, data=FORM_DATA)
    assert Comment.objects.count() == 0


def test_authorized_user_can_post_comment(author_client, news,
                                          news_detail, author):
    author_client.post(news_detail, data=FORM_DATA)
    assert Comment.objects.count() == 1
    comments = Comment.objects.get()
    assert comments.text == FORM_DATA['text']
    assert comments.author == author
    assert comments.news == news


@pytest.mark.parametrize('bad_word_data', BAD_WORD_DATA)
def test_bad_words(author_client, bad_word_data, news_detail):
    response = author_client.post(news_detail, data=bad_word_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, comment, comment_edit):
    author_client.post(comment_edit, data=FORM_DATA_EDIT_COMMENT)
    updated_comment = Comment.objects.get(pk=comment.pk)

    assert comment.news == updated_comment.news
    assert comment.author == updated_comment.author
    assert updated_comment.text == FORM_DATA_EDIT_COMMENT['text']


def test_other_user_cant_edit_comment(not_author_client, comment,
                                      comment_edit):
    response = not_author_client.post(comment_edit, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_updated = Comment.objects.get(id=comment.id)
    assert comment.author == comment_updated.author
    assert comment.text == comment_updated.text
    assert comment.news == comment_updated.news


def test_author_can_delete_comment(author_client, comment, comment_delete):
    author_client.post(comment_delete)
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_note(not_author_client, comment,
                                     comment_delete):
    response = not_author_client.post(comment_delete)
    assert Comment.objects.count() == 1
    comment_after = Comment.objects.get()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment_after.author == comment.author
    assert comment_after.text == comment.text
    assert comment_after.news == comment.news
