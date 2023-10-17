from soundscape import db, create_app  # Import the necessary modules

app = create_app()  # Create the Flask application
ctx = app.app_context()  # Create a context for the application
ctx.push()  # Push the application context

db.create_all()  # Create the database tables using SQLAlchemy's create_all() method

quit()
