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
	
class Equipment(db.Model):
	name = db.StringProperty()
	microphones = db.StringProperty()
	rostrum_microphones = db.StringProperty()
	spotlights = db.StringProperty()
	projector = db.StringProperty()
	microphone_stands = db.StringProperty()
	remarks = db.StringProperty()
