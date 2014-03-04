from google.appengine.api import users
from google.appengine.ext.ndb import Key
from app.models import User

def get_user():
    current_user = users.get_current_user()
    if current_user:
        email = current_user.email()
        q = User.query(User.email == email)
        user = q.get()
        if not user:
            user = User(email=email, level=0)
        return user

def create_login_urls(path):
    loginUrl = users.create_login_url(path)
    logoutUrl = users.create_logout_url("/")
    return loginUrl, logoutUrl
