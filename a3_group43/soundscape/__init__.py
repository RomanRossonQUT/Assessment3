from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

# Create a SQLAlchemy database instance
db = SQLAlchemy()

# Function to create and configure the Flask application
def create_app():
  app = Flask(__name__, static_url_path='/static')

  # Initialize the Bootstrap extension
  Bootstrap5(app)

  # Initialize the Bcrypt extension for password hashing
  Bcrypt(app)

  # Set the secret key for the application
  app.secret_key = 'test'

  # Configure the database URI for SQLAlchemy
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundscapedb.sqlite'

  # Initialize the SQLAlchemy database with the Flask app
  db.init_app(app)

  # Define the upload folder for images
  UPLOAD_FOLDER = '/static/img'
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

  # Initialize the LoginManager for user authentication
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'  # Set the login view
  login_manager.init_app(app)

  # Define a user loader function for LoginManager
  from .models import User
  @login_manager.user_loader
  def load_user(user_id):
      return User.query.get(int(user_id))

  # Register Blueprints for different parts of the application
  from . import views
  app.register_blueprint(views.mainbp)

  from . import events
  app.register_blueprint(events.destbp)

  from . import auth
  app.register_blueprint(auth.authbp)

  from . import api
  app.register_blueprint(api.api_bp)

  # Error handler for 404 not found errors
  @app.errorhandler(404)
  def not_found(e):
    return render_template("error.html", error=e)

  # Error handler for 500 internal server errors
  @app.errorhandler(500)
  def server_error(e):
    return render_template("error.html", error=e)

  # Error handler for 502 bad gateway errors
  @app.errorhandler(502)
  def bad_gateway(e):
    return render_template("error.html", error=e)

  # Error handler for 503 service unavailable errors
  @app.errorhandler(503)
  def service_unavailable(e):
    return render_template("error.html", error=e)

  # Error handler for 504 gateway timeout errors
  @app.errorhandler(504)
  def gateway_timeout(e):
    return render_template("error.html", error=e)

  # Context processor to provide the current year to templates
  @app.context_processor
  def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)

  return app