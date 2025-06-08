from http import HTTPStatus

from jwt import decode

from src.madr.security import create_access_token
from src.madr.settings import Settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_decode_error(client, user):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': 'Bearer invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_not_subject_email(client, user):
    data = {'test': 'test'}
    token = create_access_token(data)
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_not_user(client, user):
    data = {'sub': 'invalid user'}
    token = create_access_token(data)
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
