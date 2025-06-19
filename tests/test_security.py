from http import HTTPStatus

import pytest
from freezegun import freeze_time
from jwt import decode

from src.madr.security import create_access_token
from src.madr.settings import Settings


@pytest.mark.asyncio
async def test_jwt():
    data = {'test': 'test'}
    token = await create_access_token(data)

    decoded = decode(
        token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


@pytest.mark.asyncio
async def test_jwt_decode_error(client, user):
    response = await client.delete(
        f'/users/{user["_id"]}', headers={'Authorization': 'Bearer invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_jwt_not_subject_email(client, user):
    data = {'test': 'test'}
    token = create_access_token(data)
    response = await client.delete(
        f'/users/{user["_id"]}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_jwt_not_user(client, user):
    data = {'sub': 'invalid user 123'}
    token = create_access_token(data)
    response = await client.delete(
        f'/users/{user["_id"]}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_jwt_expired_token(client, user):
    with freeze_time('2025-01-01 12:00:00'):
        response = await client.post(
            '/auth/token',
            data={
                'username': user['email'],
                'password': user['clean_password'],
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-01-01 13:01:00'):
        response = await client.put(
            f'/users/{user["_id"]}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'test updated',
                'email': 'test@test.com',
                'password': 'secret',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
