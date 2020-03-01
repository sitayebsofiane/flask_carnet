from application.run import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    post = db.Column(db.Text)

    def __repr__(self):
        return f'username: {self.username} password{self.password} post{self.post}'