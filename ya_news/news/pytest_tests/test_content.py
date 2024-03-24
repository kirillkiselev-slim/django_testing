import pytest

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_comments_for_not_auth_user(news_detail, client):
    assert 'comments' not in client.get(news_detail).context


def test_comments_for_auth_user(news_detail, author_client, comment):
    response = author_client.get(news_detail)
    assert 'comments' in response.context
    comments = response.context['comments'][0]
    assert comment.text == comments.text
    assert comment.author == comments.author
    assert comment.news == comments.news


def test_home_page(news_on_page, news_home, client):
    news_dates = [news_on_page.date for news_on_page in
                  client.get(news_home).context['object_list']]
    assert news_dates == sorted(news_dates, reverse=True)


def test_news_comments_order(comments, news_detail, author_client):
    response = author_client.get(news_detail)
    comment_dates = [comments.created for comments in
                     response.context['comments']]
    assert comment_dates == sorted(comment_dates)
    assert isinstance(response.context['form'], CommentForm)
