from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from news.models import Comment, News


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
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
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
def comment_edit():
    return reverse('news:edit')


@pytest.fixture
def comment_delete():
    return reverse('news:delete')


# @pytest.fixture
# def pk_for_args(news):
#     return (news.id,)
#
#
# @pytest.fixture
# def pk_for_comment(comment):
#     return (comment.id,)


@pytest.fixture
def form_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'not a random comment'
    }


@pytest.fixture
def form_data_edit_comment(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'edit not a random comment'
    }


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
