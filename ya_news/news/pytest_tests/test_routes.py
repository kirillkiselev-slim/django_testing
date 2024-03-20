from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.test.client import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db

CLIENT = Client()

NOT_FOUND_STATUS = HTTPStatus.NOT_FOUND

OK_STATUS = HTTPStatus.OK

NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail')

NEWS_HOME_URL = pytest.lazy_fixture('news_home')

NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')

AUTHOR_CLIENT = pytest.lazy_fixture('author_client')

COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit')

COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete')

REDIRECT_URL_EDIT_COMMENT = pytest.lazy_fixture('redirect_url_edit_comment')

REDIRECT_URL_DELETE_COMMENT = (pytest.
                               lazy_fixture('redirect_url_delete_comment'))


@pytest.mark.parametrize(
    'url, user, expected_status',
    (
        (reverse('users:login'), CLIENT, OK_STATUS),
        (reverse('users:logout'), CLIENT, OK_STATUS),
        (reverse('users:signup'), CLIENT, OK_STATUS),
        (NEWS_DETAIL_URL, CLIENT, OK_STATUS),
        (NEWS_HOME_URL, CLIENT, OK_STATUS),
        (COMMENT_EDIT_URL, NOT_AUTHOR_CLIENT, NOT_FOUND_STATUS),
        (COMMENT_DELETE_URL, AUTHOR_CLIENT, OK_STATUS),
    ),
)
def test_pages_availability_for_users(url, user, expected_status):
    response = user.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, user, expected_redirect',
    (
        (COMMENT_EDIT_URL, CLIENT, REDIRECT_URL_EDIT_COMMENT),
        (COMMENT_DELETE_URL, CLIENT, REDIRECT_URL_DELETE_COMMENT),
    ),
)
def test_redirects(url, user, expected_redirect):
    response = user.get(url)
    assertRedirects(response, expected_redirect)
