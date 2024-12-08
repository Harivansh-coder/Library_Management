# Description: This script is used to seed the database with initial data.
from app import db
from app.models import Role, Member
from werkzeug.security import generate_password_hash


def create_initial_roles():
    """Creates the necessary roles in the database."""
    # Check if roles already exist, if not, create them
    roles = ['admin', 'librarian', 'user']
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            db.session.commit()
            print(f"Role '{role_name}' created.")
        else:
            print(f"Role '{role_name}' already exists.")


def create_initial_admin():
    """Creates the first admin member in the database."""
    admin_email = 'admin@gmail.com'
    admin_user = Member.query.filter_by(email=admin_email).first()

    if not admin_user:
        # Create the initial admin
        hashed_password = generate_password_hash(
            'password')
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            new_admin = Member(
                username='admin',
                email=admin_email,
                password=hashed_password,
                role_id=admin_role.id
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Initial admin user created.")
        else:
            print("Admin role not found, cannot create admin user.")
    else:
        print("Admin user already exists.")


def seed_database():
    """Runs all database seeding functions."""
    create_initial_roles()
    create_initial_admin()
