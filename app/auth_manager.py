# flask app
from app import app

# flask login dependency
from flask_login import LoginManager


# flask-login config
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



# User object loader func
@login_manager.user_loader
def user_loader(id):
    from app.auth.models import User
    return User.query.get(id)
