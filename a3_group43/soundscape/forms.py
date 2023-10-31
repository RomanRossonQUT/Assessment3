from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField,IntegerField,SelectField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#Create new event
class EventForm(FlaskForm):
  title = StringField('Title', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  event_date = DateField('Event Date', format='%Y-%m-%d', validators=[InputRequired()])
  start__time = TimeField('Start Time', format='%H:%M', validators=[InputRequired()])
  end__time = TimeField('End Time', format='%H:%M', validators=[InputRequired()])
  tickets_available = IntegerField('Tickets Available', validators=[InputRequired()])
  price= IntegerField('Ticket Price', validators=[InputRequired()])
  event_category = SelectField('Event Category', choices=[('rap/hip-hop', 'RAP & Hip-Hop'), ('r&b/soul', 'R&B/Soul'), ('rock', 'Rock'), ('country', 'Country')], validators=[InputRequired()])
  status = SelectField('Event Status', choices=[('open', 'Open'), ('closed', 'Closed'), ('upcoming', 'Upcoming'), ('sold-out', 'Sold out')], validators=[InputRequired()])
  submit = SubmitField("Create")
    
#User login
class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')