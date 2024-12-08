# contains all the mashmallow schemas for the app
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Role, Member, Book, BorrowedBook


class RoleSchema(SQLAlchemySchema):
    class Meta:
        model = Role
        load_instance = True  # Enable deserialization into the Role model

    id = auto_field()
    name = auto_field(required=True)
    created_at = auto_field()


class MemberSchema(SQLAlchemySchema):
    class Meta:
        model = Member
        load_instance = True

    id = auto_field()
    username = auto_field(required=True)
    email = auto_field(required=True)
    role_id = auto_field(required=True)
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
    title = auto_field(required=True)
    rating = auto_field(required=True)
    author = auto_field(required=True)
    created_at = auto_field()
    updated_at = auto_field()
    available_copies = auto_field()
    added_by = auto_field(dump_only=True)

    member = fields.Nested(MemberSchema, only=["id", "username"])


class BorrowedBookSchema(SQLAlchemySchema):
    class Meta:
        model = BorrowedBook
        load_instance = True

    id = auto_field()
    book_id = auto_field(required=True)
    member_id = auto_field(required=True)
    borrowed_at = auto_field()
    returned_at = auto_field()
    is_returned = auto_field()
    book = fields.Nested(BookSchema, only=["id", "title", "author"])
    member = fields.Nested(MemberSchema, only=["id", "username", "email"])


# Initialize the schemas for the models
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

borrowed_book_schema = BorrowedBookSchema()
borrowed_books_schema = BorrowedBookSchema(many=True)
