from django.urls import reverse
from django.conf import settings
import pytest


HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, news_bulk_create):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE



