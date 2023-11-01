from flask import Blueprint, render_template, request, redirect, url_for  # Importing necessary modules
from .models import Event  # Importing the Event model
from . import db  # Importing the database
from datetime import datetime  # Importing datetime module

# Creating a Blueprint for main routes
mainbp = Blueprint('main', __name__)

# Route for the main page
@mainbp.route('/')
def index():
    try:
        events = db.session.query(Event).all()  # Querying all events from the database
    except Exception as e:
        print(f"Error fetching events: {e}")  # Printing the error if there's an issue fetching events
        events = []  # Setting events to an empty list if there's an error

    return render_template('index.html', events=events)  # Rendering the main page template with the events

# Route for searching events by genre
@mainbp.route('/search')
def search():
    if 'search' in request.args and request.args['search'] != "":  # Checking if there is a search query
        print(request.args['search'])  # Printing the search query
        query = "%" + request.args['search'] + "%"  # Constructing a query string for the search
        try:
            events = db.session.query(Event).filter(Event.genre.like(query)).all()  # Searching events based on the genre
        except Exception as e:
            print(f"Error searching events: {e}")  # Printing the error if there's an issue searching events
            events = []  # Setting events to an empty list if there's an error

        return render_template('index.html', events=events)  # Rendering the main page template with the search results
    else:
        return redirect(url_for('main.index'))  # Redirecting to the main page if no search query is provided
