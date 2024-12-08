from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Book
from app.schemas import book_schema, books_schema
from app import db, limiter
from app.utils import role_required

books_bp = Blueprint('books', __name__)

# Create a new book
# restricted only to admin and librarian members
# Rate limit the route to 30 requests per minute


@books_bp.route('/create', methods=['POST'])
@jwt_required()
@limiter.limit("30 per minute")
@role_required(['admin', 'librarian'])
def create_book():
    data = request.json

    try:
        book = book_schema.load(data)
    except Exception as e:
        return e.messages, 400

    existing_book = Book.query.filter_by(title=book.title).first()

    if existing_book:
        return {'msg': 'Book already exists'}, 400

    new_book = Book(
        title=book.title,
        author=book.author,
        rating=book.rating,
        available_copies=book.available_copies,
        added_by=book.added_by
    )

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book), 201


# Fetch books by title or author
# Rate limit the route to 100 requests per minute
# get the books by id or title or author as query parameters

@books_bp.route('/', methods=['GET'])
@limiter.limit("100 per minute")
def get_books():

    book_id = request.args.get('id')
    title = request.args.get('title')
    author = request.args.get('author')

    query = Book.query

    # If book_id is provided, filter by book_id
    if book_id:
        query = query.filter(Book.id == book_id)

    # If title or author is provided, filter accordingly
    if title:
        # case-insensitive search
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(
            f'%{author}%'))  # case-insensitive search

    # Execute the query and fetch results
    books = query.all()

    # If no books found, return an appropriate message
    if not books:
        return {'msg': 'No books found'}, 404

    # Return the serialized book list
    return books_schema.jsonify(books), 200


# Update a book route
# restricted only to admin and librarian members
# Rate limit the route to 30
@books_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("30 per minute")
@role_required(['admin', 'librarian'])
def update_book(book_id):
    book = Book.query.get(book_id)

    if not book:
        return {'msg': 'Book not found'}, 404

    data = request.json

    try:
        # Validate and deserialize the request
        updated_book = book_schema.load(data, partial=True)
    except Exception as e:
        return e.messages, 400

    book.title = updated_book.title
    book.author = updated_book.author
    book.rating = updated_book.rating

    db.session.commit()

    return book_schema.jsonify(book), 200


# Delete a book route
# restricted only to admin and librarian members
# Rate limit the route to 30 requests per minute
@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("30 per minute")
@role_required(['admin', 'librarian'])
def delete_book(book_id):
    book = Book.query.get(book_id)

    if not book:
        return {'msg': 'Book not found'}, 404

    db.session.delete(book)
    db.session.commit()

    return {'msg': 'Book deleted successfully'}, 200
