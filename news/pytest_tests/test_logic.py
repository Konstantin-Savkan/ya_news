from http import HTTPStatus
from django.urls import reverse
from news.models import Comment
import pytest


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, id_for_args, form_data):
    url = reverse('news:detail', args=(id_for_args))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0

