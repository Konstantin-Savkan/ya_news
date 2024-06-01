from http  import HTTPStatus

from django.urls import reverse


def test_home_available_for_all(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus

