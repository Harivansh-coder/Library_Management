from . import db
from sqlalchemy.sql import func


# defining the sqlalchemy models for the database tables
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    role = db.relationship('Role', backref=db.backref('members', lazy=True))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False, default=0)
    author = db.Column(db.String(200), nullable=False, index=True)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=func.now(),
                           onupdate=func.now(), nullable=False)
    # the number of available copies of the book
    available_copies = db.Column(db.Integer, nullable=False, default=1)
    added_by = db.Column(db.Integer, db.ForeignKey(
        'member.id'), nullable=False)
    member = db.relationship('Member', backref=db.backref('books', lazy=True))


class BorrowedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'member.id'), nullable=False)
    borrowed_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    # nullable because the book may not be returned yet
    returned_at = db.Column(db.DateTime, nullable=True)
    is_returned = db.Column(db.Boolean, nullable=False, default=False)
    book = db.relationship(
        'Book', backref=db.backref('borrowed_books', lazy=True))
    member = db.relationship(
        'Member', backref=db.backref('borrowed_books', lazy=True))
