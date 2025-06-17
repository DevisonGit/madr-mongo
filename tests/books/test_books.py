from http import HTTPStatus

import pytest
from bson import ObjectId

from tests.conftest import BookFactory


@pytest.mark.asyncio
async def test_create_book(client, author, token):
    response = await client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test Testoso', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['title'] == 'test testoso'
    assert ObjectId.is_valid(response.json()['id'])


@pytest.mark.asyncio
async def test_create_book_not_token(client, author):
    response = await client.post(
        '/books/',
        headers={'Authorization': 'Bearer invalid'},
        json={'title': 'Test Testoso', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_create_book_not_author(client, author, token):
    response = await client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Testoso',
            'year': 2025,
            'author_id': str(ObjectId()),
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR'}


@pytest.mark.asyncio
async def test_create_book_already_exists(client, book, token):
    name = book.title.title()
    response = await client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': book.title,
            'year': book.year,
            'author_id': book.author_id,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': f'{name} already exists in MADR'}


@pytest.mark.asyncio
async def test_delete_book(client, author, book, token):
    response = await client.delete(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted in MADR'}


@pytest.mark.asyncio
async def test_delete_book_not_token(client, book):
    response = await client.delete(
        f'/books/{book.id}',
        headers={'Authorization': 'Bearer invalid'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_delete_book_not_found(client, book, token):
    response = await client.delete(
        f'/books/{str(ObjectId())}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


@pytest.mark.asyncio
async def test_patch_book_all_field(client, author, book, token):
    response = await client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'test helena', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'test helena',
        'year': 2025,
        'author_id': author.id,
        'id': book.id,
    }


@pytest.mark.asyncio
async def test_patch_book_one_field(client, author, book, token):
    response = await client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 2025},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': book.title,
        'year': 2025,
        'author_id': author.id,
        'id': book.id,
    }


@pytest.mark.asyncio
async def test_patch_book_not_book(client, author, book, token):
    response = await client.patch(
        f'/books/{str(ObjectId())}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test Testoso', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


@pytest.mark.asyncio
async def test_patch_book_not_author(client, author, book, token):
    response = await client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Testoso',
            'year': 2025,
            'author_id': str(ObjectId()),
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found'}


@pytest.mark.asyncio
async def test_get_book(client, author, book, token):
    response = await client.get(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': book.title,
        'year': book.year,
        'author_id': book.author_id,
        'id': book.id,
    }


@pytest.mark.asyncio
async def test_get_book_not_found(client, author, book, token):
    response = await client.get(
        f'/books/{str(ObjectId())}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


@pytest.mark.asyncio
async def test_get_books(client, author, book, token):
    response = await client.get(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'books': [
            {
                'title': book.title,
                'year': book.year,
                'author_id': book.author_id,
                'id': book.id,
            }
        ]
    }


@pytest.mark.asyncio
async def test_get_books_empty_list(client, token):
    response = await client.get(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}


@pytest.mark.asyncio
async def test_get_authors_return_5_authors(test_app, author, client, token):
    expected_books = 5
    books = [BookFactory(author_id=author.id) for _ in range(expected_books)]
    await test_app.mongodb.books.insert_many([book.dict() for book in books])
    response = await client.get(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == expected_books


@pytest.mark.asyncio
async def test_get_books_filter_title(test_app, author, client, token):
    expect_books = 1
    books = [BookFactory(author_id=author.id) for _ in range(5)]
    filtered_book = BookFactory(title='Machado 98', author_id=author.id)

    all_books = books + [filtered_book]
    await test_app.mongodb.books.insert_many([
        book.dict() for book in all_books
    ])

    response = await client.get(
        '/books/?title=Machado 98',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['books'][0]['title'] == 'Machado 98'
    assert len(response.json()['books']) == expect_books


@pytest.mark.asyncio
async def test_get_books_filter_year(test_app, author, client, token):
    expect_books = 1
    year = 1888
    books = [BookFactory(author_id=author.id) for _ in range(5)]
    filtered_book = BookFactory(year=year, author_id=author.id)

    all_books = books + [filtered_book]
    await test_app.mongodb.books.insert_many([
        book.dict() for book in all_books
    ])

    response = await client.get(
        '/books/?year=1888',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['books'][0]['year'] == year
    assert len(response.json()['books']) == expect_books


@pytest.mark.asyncio
async def test_get_books_filter_year_and_title(
    test_app, author, client, token
):
    expect_books = 1
    year = 1888
    books = [BookFactory(author_id=author.id) for _ in range(5)]
    filtered_book = BookFactory(
        title='Machado 98', year=year, author_id=author.id
    )

    all_books = books + [filtered_book]
    await test_app.mongodb.books.insert_many([
        book.dict() for book in all_books
    ])

    response = await client.get(
        '/books/?title=Machado 98&year=1888',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['books'][0]['year'] == year
    assert response.json()['books'][0]['title'] == 'Machado 98'
    assert len(response.json()['books']) == expect_books
