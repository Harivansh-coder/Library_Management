# demonstration of declaring model in Flask

# import Flask class from flask module
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create a SQLAlchemy object to connect to the database
db = SQLAlchemy()

# create a model class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), )
   
    # representation method
    def __repr__(self):
        return '<User %r>' % self.username
    
# create a Flask object to start the application
app = Flask(__name__)

# configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialize the database
db.init_app(app)

# create the database tables
with app.app_context():
    db.create_all()

def add_user():
    with app.app_context():
        user1 = User(username='admin')
        user2 = User(username='robin')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()


# run the application on the local development server
if __name__ == '__main__':

    # adding a few users to the database
    add_user()

    # run the application
    app.run(debug=True)

