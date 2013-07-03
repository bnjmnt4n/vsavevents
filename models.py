from google.appengine.ext import ndb

class Event(ndb.Model):
	name = ndb.StringProperty()
	date = ndb.DateProperty()
	start_time = ndb.TimeProperty()
	end_time = ndb.TimeProperty()
	
	# variables that shouldn't be indexed
	teacher = ndb.StringProperty(indexed=False)
	location = ndb.StringProperty(indexed=False)
	levels = ndb.StringProperty(indexed=False)
	department = ndb.StringProperty(indexed=False)
	equipment = ndb.StringProperty(indexed=False)

class User(ndb.Model):
	user = ndb.UserProperty()
	name = ndb.StringProperty()
