import pytest, pdb
from django.urls import reverse


NEWS_DETAIL = pytest.lazy_fixture('news_detail')

NEWS_HOME = pytest.lazy_fixture('news_home')


@pytest.mark.django_db
def test_comments_for_not_auth_user(client, news_detail, comment, news):
    response = client.get(NEWS_DETAIL)
    object_list = response.context['comments']
    assert comment not in object_list


def test_comments_for_auth_user(author_client, comment):
    response = author_client.get()
    object_list = response.context['comments']
    assert comment in object_list


def test_home_page(news_on_page, client, news):
    response = client.get(NEWS_HOME)
    # pdb.set_trace()
    news_dates = [news_on_page.date for news_on_page in
                  response.context['object_list']]
    assert news_dates == sorted(news_dates, reverse=True)


def test_news_comments_order(news, comments, author_client):
    response = author_client.get(NEWS_DETAIL)
    comment_dates = [comments.created for comments in
                     response.context['comments']]
    assert comment_dates == sorted(comment_dates)
