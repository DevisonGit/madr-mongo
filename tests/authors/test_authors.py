from http import HTTPStatus

import pytest

from tests.conftest import AuthorFactory


def test_create_author(client, token):
    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': '   Machado   98   '},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'name': 'machado 98', 'id': 1}


def test_create_author_exist(client, author, token):
    name = author.name.title()
    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': author.name},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': f'{name} already exists in MADR'}


def test_create_author_not_token(client, author):
    response = client.post(
        '/authors/',
        headers={'Authorization': 'Bearer invalid'},
        json={'name': 'Machado 98'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_author(client, author, token):
    response = client.delete(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Author deleted in MADR'}


def test_delete_author_not_found(client, author, token):
    response = client.delete(
        f'/authors/{author.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


def test_delete_author_not_token(client, author):
    response = client.delete(
        f'/authors/{author.id}',
        headers={'Authorization': 'Bearer invalid'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_patch_author(client, author, token):
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': '  Machado 98   '},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': 'machado 98'}


def test_patch_author_not_found(client, author, token):
    response = client.patch(
        f'/authors/{author.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': '  Machado 98   '},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


def test_patch_author_not_token(client, author):
    response = client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': 'Bearer invalid'},
        json={'name': '  Machado 98   '},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_author(client, author, token):
    response = client.get(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': author.id,
        'name': author.name,
    }


def test_get_author_not_found(client, author, token):
    response = client.get(
        f'/authors/{author.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


def test_get_authors(client, author, token):
    response = client.get(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'authors': [{'id': author.id, 'name': author.name}]
    }


@pytest.mark.asyncio
async def test_get_authors_return_5_authors(session, client, token):
    expected_authors = 5
    session.add_all(AuthorFactory.create_batch(5))
    await session.commit()
    response = client.get(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['authors']) == expected_authors


def test_get_authors_list_empty(client, token):
    response = client.get(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'authors': []}


@pytest.mark.asyncio
async def test_get_authors_filter_name(session, client, token):
    expect_authors = 1
    session.add_all(AuthorFactory.create_batch(5))
    await session.commit()
    session.add_all(AuthorFactory.create_batch(1, name='Machado 98'))
    await session.commit()

    response = client.get(
        '/authors/?name=Machado 98',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['authors']) == expect_authors
    assert response.json() == {'authors': [{'name': 'Machado 98', 'id': 6}]}
