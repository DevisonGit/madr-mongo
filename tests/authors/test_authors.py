from http import HTTPStatus

import pytest
from bson import ObjectId

from tests.conftest import AuthorFactory


@pytest.mark.asyncio
async def test_create_author(client, token):
    response = await client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': '   Machado   98   '},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'machado 98'
    assert ObjectId.is_valid(response.json()['id'])


@pytest.mark.asyncio
async def test_create_author_exist(client, author, token):
    name = author.name.title()
    response = await client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': author.name},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': f'{name} already exists in MADR'}


@pytest.mark.asyncio
async def test_create_author_not_token(client, author):
    response = await client.post(
        '/authors/',
        headers={'Authorization': 'Bearer invalid'},
        json={'name': 'Machado 98'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_delete_author(client, author, token):
    response = await client.delete(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Author deleted in MADR'}


@pytest.mark.asyncio
async def test_delete_author_not_found(client, author, token):
    response = await client.delete(
        f'/authors/{str(ObjectId())}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


@pytest.mark.asyncio
async def test_delete_author_not_token(client, author):
    response = await client.delete(
        f'/authors/{author.id}',
        headers={'Authorization': 'Bearer invalid'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_patch_author(client, author, token):
    response = await client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': '  Machado 98   '},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': 'machado 98'}


@pytest.mark.asyncio
async def test_patch_author_not_found(client, author, token):
    response = await client.patch(
        f'/authors/{str(ObjectId())}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': '  Machado 98   '},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


@pytest.mark.asyncio
async def test_patch_author_not_token(client, author):
    response = await client.patch(
        f'/authors/{author.id}',
        headers={'Authorization': 'Bearer invalid'},
        json={'name': '  Machado 98   '},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_get_author(client, author, token):
    response = await client.get(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': author.id,
        'name': author.name,
    }


@pytest.mark.asyncio
async def test_get_author_not_found(client, author, token):
    response = await client.get(
        f'/authors/{str(ObjectId())}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


@pytest.mark.asyncio
async def test_get_authors(client, author, token):
    response = await client.get(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'authors': [{'id': author.id, 'name': author.name}]
    }


@pytest.mark.asyncio
async def test_get_authors_return_5_authors(test_app, client, token):
    expected_authors = 5
    authors = [AuthorFactory() for _ in range(expected_authors)]
    await test_app.mongodb.authors.insert_many([
        author.dict() for author in authors
    ])
    response = await client.get(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['authors']) == expected_authors


@pytest.mark.asyncio
async def test_get_authors_list_empty(client, token):
    response = await client.get(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'authors': []}


@pytest.mark.asyncio
async def test_get_authors_filter_name(test_app, client, token):
    expect_authors = 1
    authors = [AuthorFactory() for _ in range(5)]
    filtered_author = AuthorFactory(name='Machado 98')

    all_author = authors + [filtered_author]

    await test_app.mongodb.authors.insert_many([
        author.dict() for author in all_author
    ])

    response = await client.get(
        '/authors/?name=Machado 98',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['authors']) == expect_authors
    assert response.json()['authors'][0]['name'] == 'Machado 98'
    assert ObjectId.is_valid(response.json()['authors'][0]['id'])
