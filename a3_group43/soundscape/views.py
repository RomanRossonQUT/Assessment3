from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db
from datetime import datetime

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    try:
        events = db.session.query(Event).all()
    except Exception as e:
        print(f"Error fetching events: {e}")
        events = []

    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    if 'search' in request.args and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        try:
            events = db.session.query(Event).filter(Event.description.like(query)).all()
        except Exception as e:
            print(f"Error searching events: {e}")
            events = []
        
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
