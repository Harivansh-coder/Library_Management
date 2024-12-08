from flask import Blueprint
from .members import members_bp
from .books import books_bp
from .borrowed_books import borrowed_books_bp

routes = Blueprint('routes', __name__)

# default route ping


@routes.route('/ping', methods=['GET'])
def ping():
    return 'pong'


# Register individual blueprints with the main routes blueprint
routes.register_blueprint(members_bp, url_prefix='/api/members')
routes.register_blueprint(books_bp, url_prefix='/api/books')
routes.register_blueprint(borrowed_books_bp, url_prefix='/api/borrowed_books')
