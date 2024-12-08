from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models import Member
from app.schemas import member_schema, members_schema
from app import limiter, db
from werkzeug.security import generate_password_hash
from app.utils import role_required

members_bp = Blueprint('members', __name__)

# Create a new member route
# restricted only to admin users
# Rate limit the route to 10 requests per minute


@members_bp.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("10/minute")
@role_required(['admin'])
def create_member():
    data = request.json

    try:
        # Validate and deserialize the request
        member = member_schema.load(data)
    except Exception as e:
        return e.messages, 400

    # Check if the member already exists
    existing_member = Member.query.filter_by(email=member.email).first()

    if existing_member:
        return {'msg': 'Member already exists'}, 400

    # Hash the password before saving
    hashed_password = generate_password_hash(member.password, method='sha256')

    # Create a new member instance with the hashed password
    new_member = Member(
        username=member.username,
        email=member.email,
        password=hashed_password,  # Set the hashed password
        role_id=member.role_id
    )

    # Add the new member to the session and commit it to the database
    db.session.add(new_member)
    db.session.commit()

    return member_schema.jsonify(new_member), 201


# Get all members route
# restricted only to admin users
# Rate limit the route to 10 requests per minute


@members_bp.route('/', methods=['GET'])
@jwt_required()
@limiter.limit("10/minute")
@role_required(['admin'])
def get_members():
    all_members = Member.query.all()
    result = members_schema.dump(all_members)
    return {'members': result}, 200


# Get a single member route
# restricted only to admin users
# Rate limit the route to 10 requests per minute

@members_bp.route('/<int:member_id>', methods=['GET'])
@jwt_required()
@limiter.limit("10/minute")
@role_required(['admin'])
def get_member(member_id):
    member = Member.query.get(member_id)

    if not member:
        return {'msg': 'Member not found'}, 404

    return member_schema.jsonify(member), 200


# Update a member route
# restricted only to admin users
# Rate limit the route to 10 requests per minute

@members_bp.route('/<int:member_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("10/minute")
@role_required(['admin'])
def update_member(member_id):
    member = Member.query.get(member_id)

    if not member:
        return {'msg': 'Member not found'}, 404

    data = request.json

    try:
        # Validate and deserialize the request
        updated_member = member_schema.load(data)
    except Exception as e:
        return e.messages, 400

    # Check if the member already exists
    existing_member = Member.query.filter_by(
        email=updated_member.email).first()

    if existing_member and existing_member.id != member_id:
        return {'msg': 'Member already exists'}, 400

    # Update the member fields
    member.username = updated_member.username
    member.email = updated_member.email
    member.role_id = updated_member.role_id

    # Commit the changes to the database
    db.session.commit()

    return member_schema.jsonify(member), 200


# Delete a member route
# restricted only to admin users
# Rate limit the route to 10 requests per minute

@members_bp.route('/<int:member_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("10/minute")
@role_required(['admin'])
def delete_member(member_id):
    member = Member.query.get(member_id)

    if not member:
        return {'msg': 'Member not found'}, 404

    db.session.delete(member)
    db.session.commit()

    return {'msg': 'Member deleted successfully'}, 200
