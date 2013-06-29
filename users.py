from google.appengine.api import users

users_string = '|demoneaux@gmail.com|weien1292@gmail.com|'

def verify_access():
	current_user = users.get_current_user()
	if users_string.find('|' + current_user.email() + '|') != -1:
		return True
	else:
		return False