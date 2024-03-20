import pytest

pytestmark = pytest.mark.django_db

NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail')

URL_DETAIL_NEWS, PK_FOR_DETAIL_NEWS = 'url', (NEWS_DETAIL_URL,)

NEWS_HOME_URL = pytest.lazy_fixture('news_home')


@pytest.mark.parametrize(URL_DETAIL_NEWS, PK_FOR_DETAIL_NEWS)
def test_comments_for_not_auth_user(client, url, comment):
    response = client.get(url)
    assert 'comments' not in response.context


@pytest.mark.parametrize(URL_DETAIL_NEWS, PK_FOR_DETAIL_NEWS)
def test_comments_for_auth_user(author_client, url, comment):
    response = author_client.get(url)
    assert 'comments' in response.context


@pytest.mark.parametrize('url', (NEWS_HOME_URL,))
def test_home_page(news_on_page, client, url):
    response = client.get(url)
    news_dates = [news_on_page.date for news_on_page in
                  response.context['object_list']]
    assert news_dates == sorted(news_dates, reverse=True)


@pytest.mark.parametrize(URL_DETAIL_NEWS, PK_FOR_DETAIL_NEWS)
def test_news_comments_order(comments, url, author_client):
    response = author_client.get(url)
    comment_dates = [comments.created for comments in
                     response.context['comments']]
    assert comment_dates == sorted(comment_dates)
