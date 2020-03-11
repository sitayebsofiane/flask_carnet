from app import db
from app.notes.models import Notebook
from app import login_manager

# note create form validation
def validate_form(title, content):
    '''
        Form validation for note creation. Validation 
        is performed according to database model.
        Rules: 
            * title, content is not nullable.
            * title can be of max. 50 chars.
            * content can be of max. 1024 chars.
    '''

    # check empty
    if not title or not content:
        return "Please fill up both fields."
    
    # validate title
    if len(title) > 50:
        return "Title can't be more than 50 characters"
    
    # validate content
    if len(content) > 1024:
        return "Content can't be more than 1024 characters."

    return ''


# Save the note form to db
def save_note_form(form, owner_id):
    note = Notebook()
    note.title = form['title']
    note.content = form['content']
    note.owner = owner_id
    db.session.add(note)
    db.session.commit()


# Top 5 notes: takes owner's id
def get_top_5_notes(id):
    """
        Returns top 5 notes according to creation date.
        Latest note will be the first one.
    """
    notes = Notebook.query.filter_by(owner=id).order_by(Notebook.created_at).all()
    notes.reverse()
    return notes[:5]


# Notes as list: takes owner's id as argument
def get_notes(id):
    """
        Returns top all notes according to creation date.
        Latest note will be the first one.
    """
    notes = Notebook.query.filter_by(owner=id).order_by(Notebook.created_at).all()
    notes.reverse()
    return notes

