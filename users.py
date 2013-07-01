from google.appengine.api import users

users_string = '|demoneaux@gmail.com|weien1292@gmail.com|wei2912.supp0rt@gmail.com|'

def get_user():
	current_user = users.get_current_user()
	if users_string.find('|' + current_user.email() + '|'):
		return current_user
	else:
		return False
