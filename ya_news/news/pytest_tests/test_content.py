from django.urls import reverse
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, args, comment_in_form',
    (
            (pytest.lazy_fixture('author_client'),
             pytest.lazy_fixture('pk_for_args'), True),
            (pytest.lazy_fixture('not_auth_client'),
             pytest.lazy_fixture('pk_for_args'), False),
    )
)
def test_comments_for_different_users(parametrized_client, args,
                                      comment_in_form, comment):
    object_list = False
    url = reverse('news:detail', args=args)
    response = parametrized_client.get(url)
    try:
        object_list = response.context['comments']
        assert (comment in object_list) is comment_in_form

    except KeyError:
        assert object_list is False


@pytest.mark.django_db
def test_home_page(news_on_page, client):
    url = reverse('news:home')
    response = client.get(url)

    object_list = response.context['object_list']
    assert len(object_list) <= 10

    news_dates = [news_on_page.date for news_on_page in object_list]
    assert news_dates == sorted(news_dates, reverse=True)


@pytest.mark.parametrize(
    'name, args',
    (
            ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
@pytest.mark.django_db
def test_news_comments_order(name, args, news, comments, author_client):
    url = reverse('news:detail', args=args)
    response = author_client.get(url)
    news_comments = response.context['comments']
    comment_dates = [comments.created for comments in news_comments]
    assert comment_dates == sorted(comment_dates)
