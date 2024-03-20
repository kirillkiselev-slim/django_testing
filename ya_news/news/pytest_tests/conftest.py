from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from news.models import Comment, News

LOGIN_URL = reverse('users:login')

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Title',
        text='Text',
        date=timezone.now()
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Random comment'
    )


@pytest.fixture
def news_detail(news):
    return reverse('news:detail', args=[news.pk])


@pytest.fixture
def news_home(news_on_page):
    return reverse('news:home')


@pytest.fixture
def comment_edit(comment):
    return reverse('news:edit', args=[comment.pk])


@pytest.fixture
def comment_delete(comment):
    return reverse('news:delete', args=[comment.pk])


@pytest.fixture
def redirect_url_edit_comment(comment):
    url = reverse('news:edit', args=[comment.pk])
    return f'{LOGIN_URL}?next={url}'


@pytest.fixture
def redirect_url_delete_comment(comment):
    url = reverse('news:delete', args=[comment.pk])
    return f'{LOGIN_URL}?next={url}'


@pytest.fixture
def comments(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Text {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()

    return comments


@pytest.fixture
def news_on_page():
    today = datetime.today()
    news = [
        News(
            title=f'Title{index}',
            text='Random news',
            date=today - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(news)

    return news
