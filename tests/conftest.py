import factory
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

from src.madr.app import app
from src.madr.authors.schemas import AuthorCreate, AuthorPublic
from src.madr.books.schemas import BookCreate, BookPublic
from src.madr.security import get_password_hash
from src.madr.users.schemas import UserCreate


class AuthorFactory(factory.Factory):
    class Meta:
        model = AuthorCreate

    name = factory.Sequence(lambda n: f'test{n}')


class UserFactory(factory.Factory):
    class Meta:
        model = UserCreate

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'<PASSWORD>{obj.username}')


class BookFactory(factory.Factory):
    class Meta:
        model = BookCreate

    title = factory.sequence(lambda n: f'name book {n}')
    year = factory.Sequence(lambda n: n + 1980)
    author_id = factory.SubFactory(AuthorFactory)


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


@pytest_asyncio.fixture
async def author(test_app):
    author_data = AuthorFactory()  # -> AuthorCreate, só com 'name'

    result = await test_app.mongodb.authors.insert_one(author_data.dict())

    # Cria um AuthorPublic com o id retornado
    return AuthorPublic(id=str(result.inserted_id), name=author_data.name)


@pytest_asyncio.fixture(autouse=True)
async def clear_authors_collection(test_app):
    await test_app.mongodb.authors.delete_many({})


@pytest_asyncio.fixture(autouse=True)
async def clear_book_collection(test_app):
    await test_app.mongodb.books.delete_many({})


@pytest_asyncio.fixture(autouse=True)
async def clear_users_collection(test_app):
    await test_app.mongodb.users.delete_many({})


@pytest_asyncio.fixture
async def book(test_app, author):
    # Cria um book com o ID do autor diretamente
    book_data = BookFactory(author_id=author.id)

    result = await test_app.mongodb.books.insert_one(book_data.dict())

    return BookPublic(
        id=str(result.inserted_id),
        title=book_data.title,
        year=book_data.year,
        author_id=book_data.author_id,
    )


@pytest_asyncio.fixture
async def other_user(test_app):
    password = 'testtest'
    user_data = UserCreate(
        username='test', email='test@example.br', password=password
    )
    user_data.password = get_password_hash(password)
    user = user_data.model_dump()

    result = await test_app.mongodb.users.insert_one(user)
    user['_id'] = str(result.inserted_id)
    user['clean_password'] = password

    return user
