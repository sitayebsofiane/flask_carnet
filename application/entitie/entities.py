class Create_entities:

    def __init__(self):
        from flask_sqlalchemy import SQLAlchemy
        from run import app
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:as122014@localhost:5432/flask'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(app)


    """ method create table user """
    def create_user(self):
        class User(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String(80), unique=True, nullable=False)
            password = self.db.Column(self.db.String(120), unique=True, nullable=False)
            post = self.db.Column(self.db.Text)

            def __repr__(self):
                return f'username: {self.username} password{self.password} post{self.post}'
