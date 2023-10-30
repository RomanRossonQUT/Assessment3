# Importing necessary modules/libraries and the database.
from flask import Blueprint, jsonify, request
from soundscape.models import Event
from . import db

# Create a Blueprint named 'api' for the API routes.
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Route to get a list of events.
@api_bp.route('/events')
def get_event():
    events = db.session.scalars(db.select(Event)).all()
    event_list = [h.to_dict() for h in events]
    return jsonify(event=event_list)

# Route to create a new event.
@api_bp.route('/events', methods=['POST'])
def create_event():
    json_dict = request.get_json()
    if not json_dict:
        return jsonify(message="No input data provided!"), 400
    event = Event(name=json_dict['name'], description=json_dict['description'],
        event_id=json_dict['event_id'])
    db.session.add(event)
    db.session.commit()
    return jsonify(message='Successfully created new event!'), 201

# Route to delete an event by its ID.
@api_bp.route('/events/<int:event>', methods=['DELETE'])
def delete_event(event_id):
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))
    db.session.delete(event)
    db.session.commit()
    return jsonify(message='Record deleted!'), 200

# Route to update an event by its ID.
@api_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    json_dict = request.get_json()
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))
    event.name = json_dict['name']
    event.description = json_dict['description']
    db.session.commit()
    return jsonify(message='Record updated!'), 200
