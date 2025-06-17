from http import HTTPStatus

import pytest
from bson import ObjectId


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['username'] == 'alice'
    assert ObjectId.is_valid(response.json()['id'])


@pytest.mark.asyncio
async def test_create_user_conflict_username(client, user):
    response = await client.post(
        '/users/',
        json={
            'username': user['username'],
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


@pytest.mark.asyncio
async def test_create_user_conflict_email(client, user):
    response = await client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': user['email'],
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


@pytest.mark.asyncio
async def test_update_user(client, user, token):
    response = await client.put(
        f'/users/{user["_id"]}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test update',
            'email': user['email'],
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user['_id'],
        'email': user['email'],
        'username': 'test update',
    }


@pytest.mark.asyncio
async def test_update_user_not_enough(client, other_user, token):
    response = await client.put(
        f'/users/{other_user["_id"]}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test update',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


@pytest.mark.asyncio
async def test_delete_user(client, user, token):
    response = await client.delete(
        f'/users/{user["_id"]}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


@pytest.mark.asyncio
async def test_delete_user_not_enough(client, other_user, token):
    response = await client.delete(
        f'/users/{other_user["_id"]}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
