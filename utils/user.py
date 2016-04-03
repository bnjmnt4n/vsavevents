from google.appengine.api import users
from app.models import User

def get_user():
    current_user = users.get_current_user()
    if current_user:
        email = current_user.email()
        query = User.query(User.email == email)
        user = query.get()
        if not user:
            user = User(email=email, level=0)
        return user

def create_login_urls(path):
    login_url = users.create_login_url(path)
    logout_url = users.create_logout_url('/')
    return login_url, logout_url
