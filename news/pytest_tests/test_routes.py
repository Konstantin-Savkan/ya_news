from http import HTTPStatus

from django.urls import reverse
import pytest


def test_home_available_for_all(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:sigup')
)
def test_pages_available_for_all(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_detail_page(client, new):
    url = reverse('news:detail', args=(new.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
