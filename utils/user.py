from google.appengine.api import users
from google.appengine.ext.ndb import Key
from models import User

def get_user():
    current_user = users.get_current_user()
    if current_user:
        email = current_user.email()

        user = User.get_or_insert(email)
        user.user = current_user
        if not user.name:
            user.name = email
        if not user.level:
            if users.is_current_user_admin():
                user.level = 2
            else:
                user.level = 0

        user.put()

        print(user)

        return user

def create_login_urls(path):
    loginUrl = users.create_login_url(path)
    logoutUrl = users.create_logout_url(path)
    return loginUrl, logoutUrl
    
def is_authorized(user):
    if user.level > 0:
        return True
    return False