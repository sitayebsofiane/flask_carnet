from app import db
from flask import url_for
from flask_login import UserMixin



# Notebook data storing model
class User(UserMixin, db.Model):
    '''
        User model is the data structure for 
        `flask auth` app to store auth user's information 

        Fields: 
            > id: Unique key to be able to identify each note 
                  seperately.
            > username: auth username
            > password: auth password
            > created_at: at the moment this model instance is created
            > update_at: moment at which it is last updated 

        Properties:
            > get_profile_url: profile link
            > get_change_password_url: password changing link
            > get_deactivate_url: account/data destroy link
    '''

    # Table name
    __tablename__ = 'users'

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # username will be generated from email address, so it's nullable 
    username = db.Column(db.String(32), nullable=True, unique=True)
    
    # email 
    email = db.Column(db.String(1024), nullable=False, unique=True)
    
    # password hashed
    password = db.Column(db.String(128), nullable=False)

    # created at
    created_at  = db.Column(    
        db.DateTime, 
        default=db.func.current_timestamp()
    )

    # updated at
    updated_at = db.Column( 
        db.DateTime, 
        default=db.func.current_timestamp(), 
        onupdate=db.func.current_timestamp()
    )

    def __str__(self):
        return self.title

    # Profile link
    @property
    def get_profile_url(self):
        return url_for('users.profile', username=self.username)
    
    # Password changing link
    @property
    def get_change_password_url(self):
        return url_for('users.change_password', username=self.username)
    
    # Destroy user & data link
    @property
    def get_deactivate_url(self):
        return url_for('users.deactivate', username=self.username)

