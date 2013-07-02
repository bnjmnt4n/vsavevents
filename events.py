from google.appengine.ext import db

class Event(db.Model):
	teacher = db.StringProperty()
	location = db.StringProperty()
	name = db.StringProperty()
	levels = db.StringProperty()
	department = db.StringProperty()
	date = db.DateProperty()
	start_time = db.TimeProperty()
	end_time = db.TimeProperty()
