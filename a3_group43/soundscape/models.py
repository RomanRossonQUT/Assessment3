# Importing necessary modules/libraries and the database.
from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pass_hash = db.Column(db.String(255), nullable=False)
    #comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    image = db.Column(db.String(400), nullable=False)
    date = db.Column(db.Date, default=datetime.now(), nullable=False)
    start_time = db.Column(db.Time, default=datetime.now(), nullable=False)
    end_time = db.Column(db.Time, default=datetime.now(), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    ticket = db.Column(db.Integer, db.ForeignKey('tickets.quantity'), nullable=False)
    #comments = db.relationship('Comment', backref='event')
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    event = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Comment: {self.text}"
    
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, db.ForeignKey('events.price'), nullable=False)
