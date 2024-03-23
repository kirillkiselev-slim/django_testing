import pytest

pytestmark = pytest.mark.django_db


def test_comments_for_not_auth_user(news_detail, client):
    assert 'comments' not in client.get(news_detail).context


def test_comments_for_auth_user(news_detail, author_client, comment):
    response = author_client.get(news_detail)
    assert 'comments' in response.context
    assert comment.text == response.context['comments'][0].text
    assert comment.author == response.context['comments'][0].author
    assert comment.created == response.context['comments'][0].created


def test_home_page(news_on_page, news_home, client):
    news_dates = [news_on_page.date for news_on_page in
                  client.get(news_home).context['object_list']]
    assert news_dates == sorted(news_dates, reverse=True)


def test_news_comments_order(comments, news_detail, author_client):
    comment_dates = [comments.created for comments in
                     author_client.get(news_detail).context['comments']]
    assert comment_dates == sorted(comment_dates)
