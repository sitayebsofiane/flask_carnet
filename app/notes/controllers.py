# flask dependencies
from flask import (
    Blueprint, 
    request, 
    render_template,
    redirect,
    abort,
    flash
)

# db
from app import db

# Notebook
from app.notes.models import Notebook

# form validation & others
from app.notes.utils import (
    validate_form, 
    save_note_form
)


# flask login: current user
from flask_login import current_user, login_required
from app import login_manager

# sorted notes utils
from app.notes.utils import get_top_5_notes, get_notes


# notes Blueprint
notes = Blueprint('notes', __name__, url_prefix='/notes')


#=================== more utilities ==================

# ownership check function
def is_owner(note_owner):
    '''Returns boolean by checking whether the user is owner of the content or not'''
    
    # is requested user == content owner?
    return note_owner == current_user.id


#=================== more utilities ==================


# ================== NOTE ROUTES =====================

# notes list view controller
@notes.route('/', methods=["GET"])
@login_required
def list():
    notes = get_notes(current_user.id)
    return render_template('notes/list.html', notes=notes)


# note create view controller
@notes.route('/create/', methods=['POST', 'GET'])
@login_required
def create():
    message = None
    notes = get_top_5_notes(current_user.id)
    
    # post request handle
    if request.method == 'POST':
        # check form 
        message = validate_form(request.form['title'], request.form['content'])

        # valid form
        if message == '':

            # success message
            message = "You note has been saved."
            
            # save form
            try:
                save_note_form(request.form, current_user.id)
            except:
                message = "Couldn't save! Something went wrong."

    # render form & top 5 notes
    return render_template('notes/create.html', message=message, notes=notes)


# note detail view controller
@notes.route('/<int:id>/', methods=['GET'])
@login_required
def detail(id):
    note = Notebook.query.get_or_404(id)
    
    # ownership check
    if not is_owner(note.owner):
        flash("You are not authorized for this content")
        return redirect('/')
    return render_template('notes/detail.html', note=note)


# note update view controller
@notes.route('/<int:id>/update/', methods=['GET', 'POST'])
@login_required
def update(id):

    note = Notebook.query.get_or_404(id); message = None

    # owner check
    if not is_owner(note.owner):
        flash("You are not authorized for this content")
        return redirect('/')
    
    # post request handle
    if request.method == 'POST':

        # validate data
        if validate_form(request.form['title'], request.form['content']) == '':
            
            # update
            note.title = request.form['title']
            note.content = request.form['content']
            
            # save
            try:
                db.session.add(note)
                db.session.commit()
                message = 'Successfully updated.'
            except: 
                message = "Couldn't update!"
    return render_template('notes/update.html', note=note, message=message)


# note delete view controller
@notes.route('/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
def delete(id):
    note = Notebook.query.get_or_404(id)

    # owner check
    if not is_owner(note.owner):
        flash("You are not authorized for this content")
        return redirect('/')
    
    # post requst handle
    if request.method == 'POST':
        delete = request.form['delete']
        
        # delete
        if delete == '1':
            
            # delete object from db
            db.session.delete(note)
            db.session.commit()
            return redirect('/notes/')
        else:
            return redirect('/notes/%s/'%(note.id))
    return render_template('notes/delete.html', note=note)


