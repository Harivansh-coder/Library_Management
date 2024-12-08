# contains all the mashmallow schemas for the app
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Role, Member, Book, BorrowedBook


class RoleSchema(SQLAlchemySchema):
    class Meta:
        model = Role
        load_instance = True  # Enable deserialization into the Role model

    id = auto_field()
    name = auto_field()
    created_at = auto_field()


class MemberSchema(SQLAlchemySchema):
    class Meta:
        model = Member
        load_instance = True

    id = auto_field()
    username = auto_field()
    email = auto_field()
    role_id = auto_field()
    # Prevent password from being serialized
    password = fields.String(load_only=True)
    created_at = auto_field()
    updated_at = auto_field()
    role = fields.Nested(RoleSchema)  # Serialize the role relationship


class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = auto_field()
    title = auto_field()
    rating = auto_field()
    author = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    available_copies = auto_field()
    added_by = auto_field()
    member = fields.Nested(MemberSchema, only=["id", "username"])


class BorrowedBookSchema(SQLAlchemySchema):
    class Meta:
        model = BorrowedBook
        load_instance = True

    id = auto_field()
    book_id = auto_field()
    member_id = auto_field()
    borrowed_at = auto_field()
    returned_at = auto_field()
    is_returned = auto_field()
    book = fields.Nested(BookSchema, only=["id", "title", "author"])
    member = fields.Nested(MemberSchema, only=["id", "username", "email"])
