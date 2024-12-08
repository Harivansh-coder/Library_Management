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
@role_required('admin')
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
@role_required('admin')
def get_members():
    all_members = Member.query.all()
    result = members_schema.dump(all_members)
    return {'members': result}, 200
