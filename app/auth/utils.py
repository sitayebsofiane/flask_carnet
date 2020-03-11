# database object
from app import db

# auth model
from app.auth.models import User

# password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# flask dependencies
from flask import url_for

# utils
import re
import string
import random



# generates random strings
def generate_random_str(size=1, numonly=False):
    elems = string.ascii_lowercase + string.digits
    if numonly: elems = string.digits
    return ''.join(random.choice(elems) for _ in range(size))


# valid email check
def valid_email(email):
    fmt = bool(re.compile(r"([a-z0-9._]+@[a-z]+.[a-z]+)").match(email))
    
    # format is ok i.e. user@company.extension
    if fmt:
        username = email.split('@')[0]
        company, ext = email.split('@')[1].split('.')
        
        # valid email check: usr@mail.com
        if len(username) < 3 or len(company) < 4 or len(ext) < 3:
            return False
        return True
    return False


# Generate username
def generate_unique_username(username):
    '''Generates unique username for User data model from a given username.'''
    # user already exist
    if User.query.filter_by(username=username).first():
        
        # update username
        username += generate_random_str(size=1, numonly=True)
        
        # recursion
        return generate_unique_username(username)
    
    # return the unique username
    return username


# E-mail already exist check
def email_exist(email):
    if User.query.filter_by(email=email).first():
        return True
    return False


# Validate register form
def validate_register_form(form):
    email = form['email']
    passwd = form['password']
    re_passwd = form['re-password']
    
    # did not fill all the fields
    if not email or not passwd or not re_passwd: return "Please fill up all fields."
    
    # invalid email
    if not valid_email(email): return "Please choose a valid email."
    
    # email already exists
    if email_exist(email): return "Email already exists. <a href='%s'>login</a> now."%(url_for('auth.login'))
    
    # invalid password length
    if len(passwd) < 6: return "Please choose a longer password."
    
    # password didn't match
    if passwd != re_passwd: return "Password didn't match."
    
    # no error
    return ''
    

# create new user from register form
def create_new_auth_user(form):
    user = User()
    user.email = form['email']
    user.username = generate_unique_username(form['email'].split('@')[0])
    user.password = generate_password_hash(form['password'], method='sha256')
    
    # saving to database
    db.session.add(user)
    db.session.commit()


