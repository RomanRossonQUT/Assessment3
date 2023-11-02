from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm
from datetime import datetime
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
    event = Event(title=form.title.data,
                  description=form.description.data,
                  venue=form.venue.data,
                  date=form.event_date.data,
                  start_time=form.start__time.data, 
                  end_time=form.end__time.data,
                  status=form.status.data,
                  price=form.price.data,
                  genre=form.event_category.data,
                  tickets_available=form.tickets_available.data,
                  image=db_file_path)
    db.session.add(event)
    db.session.commit()
    flash('Successfully created new event!', 'success')
    return redirect(url_for('main.index'))
  return render_template('events/create.html', form=form)

def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename 
    BASE_PATH = os.path.dirname(__file__)
    upload_directory = os.path.join(BASE_PATH, 'static', 'image')
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory) 
    upload_path = os.path.join(upload_directory, secure_filename(filename))
    db_upload_path = '/static/image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      comment = Comment(description=form.description.data,
                        event=event,
                        user=current_user) 
      db.session.add(comment) 
      db.session.commit() 
      flash('Your comment has been added.', 'success')  
    return redirect(url_for('event.show', id=id))

@destbp.route('/<id>/comment/delete/<comment_id>', methods=['POST'])
@login_required
def delete_comment(id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment:
        if comment.user.username == current_user.username:
            db.session.delete(comment)
            db.session.commit()
            flash('Comment deleted successfully.', 'success')
        else:
            flash('You are not authorized to delete this comment.', 'error')
    return redirect(url_for('event.show', id=id))

@destbp.route('/<id>/book', methods=['POST'])
@login_required
def book_event(id):
    event = Event.query.get(id)
    if event:
        type = request.form['type']
        quantity = int(request.form['quantity'])

        if quantity > event.tickets_available:
            flash('Tickets not available. Please try booking a lower quantity.', 'error')
            return redirect(url_for('event.show', id=id))
        booking = Booking(
            user=current_user,
            event=event,
            type=type,
            quantity=quantity,
            booking_date=datetime.now())
        db.session.add(booking)
        event.tickets_available -= quantity
        db.session.commit()
        flash('Event booked successfully.', 'success')
    else:
        flash('Event not found.', 'error')
    return redirect(url_for('event.show', id=id))

@destbp.route('/booking-history')
@login_required
def booking_history():
    # Query the database to get the booking history of the current user
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('booking_history.html', bookings=bookings)