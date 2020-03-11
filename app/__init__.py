# Import flask and template operators
from flask import (
    Flask, 
    render_template,
    request
)

# CSRF protection
from flask_wtf.csrf import CSRFProtect

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# template filters (custom): to use in jinja/flask template
from app import filters

# flask login dependency
from app import auth_manager as login_manager
from flask_login import current_user

# App configs: Takes config key & values from config.py 
# file's variables & values
app.config.from_object('config')

# include CSRF protection to flask application
csrf = CSRFProtect(app)

# Database object
db = SQLAlchemy(app)

# Notebook model
from app.notes.utils import get_top_5_notes

# Notes module/component using its blueprint handler
from app.notes.controllers import notes as notes_controller
from app.auth.controllers import auth as auth_controller

# Blueprints for routes: auth, notes
app.register_blueprint(notes_controller)
app.register_blueprint(auth_controller)

# 404 error handler
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

# index route
@app.route('/', methods=['GET'])
def index():

    # if not auth user render guest.html
    if not current_user.is_authenticated:
        return render_template('guest.html')
    notes = get_top_5_notes(current_user.id)
    return render_template('index.html', notes=notes)


# create the database
db.create_all()
