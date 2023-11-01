# Importing necessary modules/libraries and the database.
from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    pass_hash = db.Column(db.String(255))
    #comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(400))
    image = db.Column(db.String(400))
    date = db.Column(db.Date, default=datetime.now())
    status = db.Column(db.String(50))
    price = db.Column(db.Float)
    genre = db.Column(db.String(100))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    tickets_available = db.Column(db.Integer)
    #ticket = db.Column(db.String(50), db.ForeignKey('tickets.event'))
    #comments = db.relationship('Comment', backref='event')

    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.now())
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    user = db.Column(db.String(100), db.ForeignKey('users.username'))

    def __repr__(self):
        return f"Comment: {self.text}"
    
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), db.ForeignKey('users.username'))
    #event = db.Column(db.String(50), db.ForeignKey('events.id'))
    quantity = db.Column(db.Integer)
    #price = db.Column(db.Integer, db.ForeignKey('events.price'))
