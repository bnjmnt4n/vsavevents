from google.appengine.api import users
from google.appengine.ext.ndb import Key
from models import User

users_string = '|demoneaux@gmail.com|weien1292@gmail.com|wei2912.supp0rt@gmail.com|ernestdummyinthecity@gmail.com|ivantangwm@gmail.com|jethrophuah@gmail.com|uberstrike12345@gmail.com|ryantan996@hotmail.com|isaac.ng.jy@gmail.com|marcoseah@gmail.com|target2033@gmail.com|gnekaraalhad@gmail.com|'

def get_user():
	current_user = users.get_current_user()
	if current_user:
		email = current_user.email()
		if users_string.find('|' + email + '|') != -1:
			user = User.get_or_insert(email)
			user.user = current_user
			user.put()
			return current_user
		else:
			return False
	else:
		return False

def create_login_urls(path):
	loginUrl = users.create_login_url(path)
	logoutUrl = users.create_logout_url(path)
	return loginUrl, logoutUrl