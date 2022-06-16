from app import db,login
from flask_login import UserMixin # only for the user model
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


poketeam = db.Table("poketeam",
    db.Column("pokemon_id", db.Integer, db.ForeignKey('pokemon.pokemon_id')),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    pokemon = db.relationship(
        "Pokemon",
        secondary=poketeam,
        backref="poketeam",
        lazy="dynamic",
        )
    token = db.Column(db.String, index=True, unique=True)
    token_exp = db.Column(db.DateTime)

    ##### methods for tokens
    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        # give user back their token if token is still valid
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        # if token doesn't exist or is expired
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    # we won't use this but it's pretty important to have in real world
    def revoke_token(self):
        current_time = dt.utcnow()
        self.token_exp = current_time - timedelta(seconds=61)

    @staticmethod
    def check_token(token):
        u = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

    ##### methods for tokens ^
    
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

    def catch_em(self, poke):
        self.poketeam.append(poke) #interact with the join table
        db.session.commit() #save to the table

    def release(self, poke):
        self.poketeam.remove(poke)
        db.session.commit()

    def showteam(self):
        self_pokemon = self.poketeam
        fullteam = Pokemon.query.join(poketeam, (Pokemon.user_id == poketeam.c.user_id)).filter(poketeam.c.poke_id == self.id)
        pokemon_team = fullteam.union(self_pokemon).order_by(Pokemon.name)
        return pokemon_team

class Pokemon(db.Model):
    pokemon_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    base_exp = db.Column(db.Integer)
    sprite = db.Column(db.String)
    ability = db.Column(db.String)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)

    def from_dict(self, data):
        self.name = data['name']
        self.base_exp = data['base_exp']
        self.sprite = data['sprites']
        self.ability = data['ability']
        self.hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']

    def save(self):
        db.session.add(self) #adds the post to the db session
        db.session.commit() #save everything in the session to the db




    


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # equivalent to saying SELECT * FROM User WHERE id = ???

