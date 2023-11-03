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
    contact_number = db.Column(db.Integer)
    home_address = db.Column(db.String(400))

    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(400))
    image = db.Column(db.String(400))
    venue = db.Column(db.String(100))
    date = db.Column(db.Date, default=datetime.now())
    status = db.Column(db.String(50))
    price = db.Column(db.Float)
    genre = db.Column(db.String(100))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    tickets_available = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='events', lazy=True)

    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.now())
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event', backref='comments', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='comments', lazy=True)

    def __repr__(self):
        return f"Comment: {self.text}"

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='bookings', lazy=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event', backref='bookings', lazy=True)
    type = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    booking_date = db.Column(db.DateTime, default=datetime.now())