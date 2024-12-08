from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models import Member

# this decorator checks if the user is an particular role


def role_required(role: list):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = Member.query.filter_by(
                email=get_jwt_identity()).first()
            if current_user.role.name not in role:
                return jsonify(msg='Unauthorized'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
