from http import HTTPStatus

import pytest
from freezegun import freeze_time


@pytest.mark.asyncio
async def test_get_token(client, user):
    response = await client.post(
        '/auth/token',
        data={
            'username': user['email'],
            'password': user['clean_password'],
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


@pytest.mark.asyncio
async def test_get_token_not_user(client, user):
    response = await client.post(
        '/auth/token',
        data={'username': 'not valid', 'password': user['clean_password']},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


@pytest.mark.asyncio
async def test_get_token_not_verify_password(client, user):
    response = await client.post(
        '/auth/token',
        data={'username': user['email'], 'password': 'not valid'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


@pytest.mark.asyncio
async def test_refresh_token(client, user, token):
    response = await client.post(
        '/auth/refresh-token', headers={'Authorization': f'Bearer {token}'}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_token_expired_dont_refresh(client, user):
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
        response = await client.post(
            '/auth/refresh-token', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
