from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

destbp = Blueprint('event', __name__, url_prefix='/events')

@destbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    form = CommentForm()    
    return render_template('events/show.html', event=event, form=form)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    event = Event(title=form.title.data, description=form.description.data,
                  date=form.event_date.data, start_time=form.start__time.data, 
                  end_time=form.end__time.data, status=form.status.data,
                  price=form.price.data, genre=form.event_category.data,
                  ticket=form.tickets_available.data,
    image=db_file_path)
    db.session.add(event)
    db.session.commit()
    flash('Successfully created new event!', 'success')
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename 
    BASE_PATH = os.path.dirname(__file__)
    upload_directory = os.path.join(BASE_PATH, 'static', 'db_image')
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory) 
    upload_path = os.path.join(upload_directory, secure_filename(filename))
    db_upload_path = '/static/db_image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      comment = Comment(text=form.text.data, event=event,
                        user=current_user) 
      db.session.add(comment) 
      db.session.commit() 
      flash('Your comment has been added', 'success')  
    return redirect(url_for('event.show', id=id))