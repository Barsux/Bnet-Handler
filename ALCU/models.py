from ALCU import db, app
from flask_login import UserMixin, LoginManager
manager = LoginManager(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(10), unique = True)
    email = db.Column(db.String(20), unique = True)
    psw = db.Column(db.String(500), nullable=True)
    def __repr__(self):
        return f"<User {self.id}>"


    def __init__(self, login, email, psw):
        self.login = login
        self.email = email
        self.psw = psw
@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

    

