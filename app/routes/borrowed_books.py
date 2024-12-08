from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import BorrowedBook, Book, Member
from app.schemas import borrowed_book_schema, borrowed_books_schema
from app import db, limiter
from datetime import datetime
from app.utils import role_required

borrowed_books_bp = Blueprint('borrowed_books', __name__)

# Borrow a book

# Limit the number of requests to 50 per minute
# only librarian and admin can issue a book to a member


@borrowed_books_bp.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
@role_required(['admin', 'librarian'])
def borrow_book():
    data = request.get_json()
    book_id = data.get('book_id')
    member_id = data.get('member_id')
    book = Book.query.get(book_id)
    member = Member.query.get(member_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    if book.available_copies == 0:
        return jsonify({'message': 'All copies of the book have been borrowed'}), 400

    borrowed_book = BorrowedBook.query.filter_by(
        book_id=book_id, member_id=member_id, is_returned=False).first()
    if borrowed_book:
        return jsonify({'message': 'Book already borrowed by the member'}), 400

    borrowed_book = BorrowedBook(book_id=book_id, member_id=member_id)
    book.available_copies -= 1
    db.session.add(borrowed_book)
    db.session.commit()

    return borrowed_book_schema.jsonify(borrowed_book), 201

# Return a borrowed book
# only librarian and admin can return a issued book


@borrowed_books_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'librarian'])
@role_required(['admin', 'librarian'])
def return_book(id):
    borrowed_book = BorrowedBook.query.get(id)
    if not borrowed_book:
        return jsonify({'message': 'Borrowed book not found'}), 404
    if borrowed_book.is_returned:
        return jsonify({'message': 'Book already returned'}), 400
    borrowed_book.is_returned = True
    borrowed_book.returned_at = datetime.now()
    book = Book.query.get(borrowed_book.book_id)
    book.available_copies += 1
    db.session.commit()
    return borrowed_book_schema.jsonify(borrowed_book), 200

# Get all borrowed books
# All users can view borrowed books


@borrowed_books_bp.route('/', methods=['GET'])
@jwt_required()
def get_borrowed_books():

    # current user id
    current_user_id = get_jwt_identity()

    # get all borrowed books for the current user id
    borrowed_books = BorrowedBook.query.filter_by(
        member_id=current_user_id).all()

    return jsonify(borrowed_books_schema.dump(borrowed_books)), 200

# Get all borrowed books from the library
# only librarian and admin can view all borrowed books


@borrowed_books_bp.route('/all', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_all_borrowed_books():
    borrowed_books = BorrowedBook.query.all()
    return jsonify(borrowed_books_schema.dump(borrowed_books)), 200
