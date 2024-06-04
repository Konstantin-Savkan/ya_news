import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.test.client import Client
from news.models import Comment, News
from news.forms import BAD_WORDS, WARNING

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'

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
    news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return news


@pytest.fixture
def id_for_args(news):
    return (news.id,)


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        text=COMMENT_TEXT,
        news=news,
        author=author
    )
    return comment


@pytest.fixture
def id_comment_for_args(comment):
    return (comment.id,)


@pytest.fixture
def news_bulk_create():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    news_bulk_create = News.objects.bulk_create(all_news)
    return news_bulk_create


@pytest.fixture
def news_with_comment(author):
    news = News.objects.create(
        title='Тестовая новость', text='Просто текст.'
    )
    detail_url = reverse('news:detail', args=(news.id,))
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return detail_url


@pytest.fixture
def form_data():
    form_data = {'text': NEW_COMMENT_TEXT}
    return form_data
