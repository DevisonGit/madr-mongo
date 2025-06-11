from http import HTTPStatus

import pytest

from tests.conftest import BookFactory


def test_create_book(client, author, token):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test Testoso', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'test testoso',
        'year': 2025,
        'author_id': author.id,
        'id': 1,
    }


def test_create_book_not_token(client, author):
    response = client.post(
        '/books',
        headers={'Authorization': 'Bearer invalid'},
        json={'title': 'Test Testoso', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_create_book_not_author(client, author, token):
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Testoso',
            'year': 2025,
            'author_id': author.id + 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found'}


@pytest.mark.asyncio
async def test_create_book_already_exists(client, author, book, token):
    name = book.title.title()
    response = client.post(
        '/books',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': book.title,
            'year': book.year,
            'author_id': author.id,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': f'{name} already exists in MADR'}


def test_delete_book(client, book, token):
    response = client.delete(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted in MADR'}


def test_delete_book_not_token(client, book):
    response = client.delete(
        f'/books/{book.id}',
        headers={'Authorization': 'Bearer invalid'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_book_not_found(client, book, token):
    response = client.delete(
        f'/books/{book.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


def test_patch_book_all_field(client, author, book, token):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test Testoso', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'test testoso',
        'year': 2025,
        'author_id': author.id,
        'id': 1,
    }


def test_patch_book_one_field(client, author, book, token):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': 2025},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': book.title,
        'year': 2025,
        'author_id': author.id,
        'id': 1,
    }


def test_patch_book_not_book(client, author, book, token):
    response = client.patch(
        f'/books/{book.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test Testoso', 'year': 2025, 'author_id': author.id},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


def test_patch_book_not_author(client, author, book, token):
    response = client.patch(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Testoso',
            'year': 2025,
            'author_id': author.id + 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found'}


def test_get_book(client, author, book, token):
    response = client.get(
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


def test_get_book_not_found(client, author, book, token):
    response = client.get(
        f'/books/{book.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found in MADR'}


def test_get_books(client, author, book, token):
    response = client.get(
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


def test_get_books_empty_list(client, token):
    response = client.get(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}


@pytest.mark.asyncio
async def test_get_authors_return_5_authors(session, client, token):
    expected_books = 5
    session.add_all(BookFactory.create_batch(5))
    await session.commit()
    response = client.get(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == expected_books


@pytest.mark.asyncio
async def test_get_books_filter_title(session, client, token):
    expect_books = 1
    session.add_all(BookFactory.create_batch(5))
    await session.commit()
    session.add_all(BookFactory.create_batch(1, title='The Machado 98'))
    await session.commit()

    response = client.get(
        '/books/?title=The Machado 98',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'books': [
            {'year': 2001, 'title': 'The Machado 98', 'author_id': 1, 'id': 6}
        ]
    }
    assert len(response.json()['books']) == expect_books


@pytest.mark.asyncio
async def test_get_books_filter_year(session, client, token):
    expect_books = 1
    session.add_all(BookFactory.create_batch(5))
    await session.commit()
    session.add_all(BookFactory.create_batch(1, year=2025))
    await session.commit()

    response = client.get(
        '/books/?year=2025',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'books': [
            {'year': 2025, 'title': 'name book 27', 'author_id': 1, 'id': 6}
        ]
    }
    assert len(response.json()['books']) == expect_books


@pytest.mark.asyncio
async def test_get_books_filter_year_and_title(session, client, token):
    expect_books = 1
    session.add_all(BookFactory.create_batch(5))
    await session.commit()
    session.add_all(BookFactory.create_batch(1, title='Test', year=2025))
    await session.commit()

    response = client.get(
        '/books/?title=Test&year=2025',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'books': [{'year': 2025, 'title': 'Test', 'author_id': 1, 'id': 6}]
    }
    assert len(response.json()['books']) == expect_books
