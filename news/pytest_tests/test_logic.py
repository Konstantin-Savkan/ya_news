from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError
from news.models import Comment
from news.forms import BAD_WORDS, WARNING
import pytest

#NEW_COMMENT_TEXT = 'Обновлённый комментарий'


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, id_for_args, form_data):
    url = reverse('news:detail', args=(id_for_args))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_user_can_create_comment(
    author_client, author, news, id_for_args, form_data
):
    url = reverse('news:detail', args=(id_for_args))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, id_for_args):
    url = reverse('news:detail', args=(id_for_args))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, id_for_args, comment):
    news_url = reverse('news:detail', args=(id_for_args))
    url_to_comments = news_url + '#comments'
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_not_author_cant_delete_comment(not_author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_author_can_edit_comment(
        author_client, id_for_args,
        comment, form_data
):
    news_url = reverse('news:detail', args=(id_for_args))
    url_to_comments = news_url + '#comments'
    edit_url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(edit_url, data=form_data)
    comment.refresh_from_db()
    assertRedirects(response, url_to_comments)
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, form_data
):
    edit_url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != form_data['text']
