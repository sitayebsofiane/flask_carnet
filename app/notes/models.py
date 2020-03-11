from app import db
from app.auth.models import User
from flask_sqlalchemy import SQLAlchemy
from flask import url_for


# Notebook data storing model
class Notebook(db.Model):
    '''
        Notebook model is the data structure for 
        `flask notebook` application to store notes 
        according to this very data model.

        Fields: 
            > id: U=unique key to be able to identify each note 
                  seperately.
            > title: title of the note. String of size 50, more 
                     than 50 character(s) will be escaped.
            > content: note content of maximum size 1024, more 
                       than 1024 character(s) will not saved
            > created: the moment when the `Notebook` model 
                       instance is being stored.

        Properties:
            > get_owner: returns username of the owner of the note
            > get_shortened_title: gives title of 20 characters.
            > get_absolute_url: gives detail view link for the note.
            > get_update_url: gives update view link for the note.
            > get_delete_url: gives delete view link for the note.
    '''

    # Table name
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1024), nullable=False)

    # user's id 
    owner = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<Notebook %r>' % self.id

    # Returns when `Notebook` model is being called/show
    def __str__(self):
        return self.title
    
    # owner's username
    @property
    def get_owner(self):
        usr = User.query.get(self.owner)
        return usr.username

    # Shortened title
    @property
    def get_shortened_title(self):
        return self.title[:20]
    
    # Detail link
    @property
    def get_absolute_url(self):
        return url_for('notes.detail', id=self.id)
    
    # Update link
    @property
    def get_update_url(self):
        return url_for('notes.update', id=self.id)
    
    # Delete link
    @property
    def get_delete_url(self):
        return url_for('notes.delete', id=self.id)
    
