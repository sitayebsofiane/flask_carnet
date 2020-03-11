# flask dependencies
from flask import (
    Blueprint, 
    request, 
    render_template,
    redirect,
    abort,
    flash,
    url_for
)

# password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# db
from app import db


# Notebook & auth models
from app.auth.models import User


# form validation & others
from app.auth.utils import (
    validate_register_form,
    create_new_auth_user,
)

# auth Blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')

# flask-login dependencies
from flask_login import (
    login_user, 
    current_user, 
    login_required, 
    logout_user
)

# notebook model
from app.notes.models import Notebook

# login manager
from app import login_manager


# ================== NOTE ROUTES =====================

# Logout view controller
@auth.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


# Login view controller
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    
    # logged in redirect
    if current_user.is_authenticated: 
        flash("Please <a href='%s'>log out</a> and try again."%(url_for('auth.logout')))
        return redirect('/')
    
    # post request handle
    if request.method == 'POST':
        usr = request.form['usr']
        passwd = request.form['password']
        
        # check user exist or not
        user = User.query.filter_by(email=usr).first()
        if not user: user = User.query.filter_by(username=usr).first()
        
        # unknown username/email
        if not user:
            flash("Incorrect login credentials.")
        else:
            
            # check password
            if not check_password_hash(user.password, passwd):
                flash("Incorrect login credentials.")
            else:
                
                # login user
                login_user(user)
                flash("You are successfully logged in.")
                
                # return to profile
                return redirect(url_for('auth.profile'))
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


# register view controller
@auth.route('/register/', methods=['GET', 'POST'])
def register():
    
    # logged in redirect
    if current_user.is_authenticated: return redirect('/')

    if request.method == 'POST':

        # validation 
        message = validate_register_form(request.form)

        # success response
        if message == '':
            try:
                create_new_auth_user(request.form)
                flash("<span class='alert-link'>Congrats!</span> You are a new member now. Login here.") # success message
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash("Something went wrong. Try again.") # Couldn't save to db
        else:
            # send error message
            flash(message)

        # redirect to prevent reload-resubmit post request
        return redirect(url_for('auth.register'))
    return render_template('auth/register.html')


# profile view controller
@auth.route('/profile/', methods=['GET'])
@login_required
def profile():
    notes = Notebook.query.filter_by(owner=current_user.id).all()
    return render_template('auth/profile.html', 
                            user=current_user, 
                            note_counter = len(notes))


# change password controller {yet to complete}
@auth.route('/<string:username>/change-password/', methods=['GET', 'POST'])
@login_required
def change_password(username):
    return render_template('auth/change-password.html')


# deactivate/delete user & data view controller
@auth.route('/<string:username>/deactivate/', methods=['GET', 'POST'])
@login_required
def deactivate(username):
    return render_template('auth/deactivate.html')
