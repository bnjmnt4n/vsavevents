from google.appengine.api import users
from google.appengine.ext.ndb import Key
from models import User

def get_user():
    current_user = users.get_current_user()
    if current_user:
        email = current_user.email()
        q = User.query(User.email == email)
        user = q.get()
        if not user:
            user = User(name=email, email=email, level=0)
            if users.is_current_user_admin():
                user.level = 2
        return user

def create_login_urls(path):
    loginUrl = users.create_login_url(path)
    logoutUrl = users.create_logout_url(path)
    return loginUrl, logoutUrl