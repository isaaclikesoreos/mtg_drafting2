from datetime import datetime
from application import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Cube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), default=None)
    cube_mainboard = db.Column(db.Text, nullable=False)
    cube_sideboard = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Cube {self.name}>"

class CardInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(101), unique=True, nullable=False)
    mana_cost = db.Column(db.String(25))
    type_line = db.Column(db.String(75))
    image = db.Column(db.String(256))

    def __repr__(self):
        return f"<CardInfo ('{self.card_name}','{self.id}', '{self.mana_cost}', '{self.type_line}', '{self.image}'>"

class ActiveCubeDecks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(101), db.ForeignKey('card_info.card_name'), unique=True, nullable=False)
    mana_cost = db.Column(db.String(25), db.ForeignKey('card_info.mana_cost'))
    type_line = db.Column(db.String(75), db.ForeignKey('card_info.type_line'))
    image = db.Column(db.String(256), db.ForeignKey('card_info.image'))
    card_id = db.Column(db.Integer, db.ForeignKey('card_info.id'), unique=True, nullable=False)

    def __repr__(self):
        return f"<Active_Cube_Deck ('{self.card_name}','{self.id}', '{self.mana_cost}', '{self.type_line}', '{self.image}', '{self.card_id}')>"
