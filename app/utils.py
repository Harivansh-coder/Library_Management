from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models import Member

# this decorator checks if the user is an particular role


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()

            user = Member.query.get(current_user_id)

            if user.role != role:
                return jsonify(msg='Unauthorized user'), 403
            return f(*args, **kwargs)

        return decorated_function
    return decorator
