from app import db,login
from flask_login import UserMixin # only for the user model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    
    # repr should return a unique identifying string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    # human readable version
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    # salts and hashes password for security
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares user password to the password provided
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    # save the user to the database
    def save(self):
        db.session.add(self) # adds the user to the db session
        db.session.commit() # saves everything to the db session

# not really part of the model but makes sense to add it here
# user loader

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # equivalent to saying SELECT * FROM User WHERE id = ???