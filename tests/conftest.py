import factory
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

from src.madr.app import app
from src.madr.security import get_password_hash
from src.madr.users.schemas import UserCreate


class UserFactory(factory.Factory):
    class Meta:
        model = UserCreate

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'<PASSWORD>{obj.username}')


@pytest.fixture(scope='session')
def mongo_container():
    """Configura o contêiner MongoDB para os testes."""
    with MongoDbContainer('mongo:latest') as mongo:
        yield mongo


@pytest_asyncio.fixture
async def test_app(mongo_container):
    app.mongodb_client = AsyncIOMotorClient(
        mongo_container.get_connection_url()
    )
    app.mongodb = app.mongodb_client.test_db
    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture
async def client(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture
async def user(test_app):
    password = 'testtest'
    user_data = UserCreate(
        username='testuser', email='test@example.com', password=password
    )
    user_data.password = get_password_hash(password)
    user = user_data.model_dump()

    result = await test_app.mongodb.users.insert_one(user)
    user['_id'] = str(result.inserted_id)
    user['clean_password'] = password

    return user


@pytest_asyncio.fixture
async def token(client, user):
    response = await client.post(
        '/auth/token',
        data={'username': user['email'], 'password': user['clean_password']},
    )
    return response.json()['access_token']
