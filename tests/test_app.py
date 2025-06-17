from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_root_return_ok_and_madr(client):
    response = await client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'MADR'}
