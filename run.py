# entry point for the application
from app import create_app, db
from app.models import Member
from scripts.initiate_db import seed_database


app = create_app()

# running the database seeding function


def initialize_database():

    # Create the database tables and seed the database
    db.create_all()
    print("Database tables created successfully.")
    if not db.session.query(Member).first():
        seed_database()


if __name__ == '__main__':

    with app.app_context():
        initialize_database()
    app.run(debug=True)
