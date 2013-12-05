from google.appengine.ext import ndb

class Event(ndb.Model):
	name = ndb.StringProperty()
	date = ndb.DateProperty()
	start_time = ndb.TimeProperty()
	end_time = ndb.TimeProperty()
	
	teacher = ndb.StringProperty(indexed=False)
	location = ndb.StringProperty(indexed=False)
	levels = ndb.StringProperty(indexed=False)
	equipment = ndb.StringProperty(indexed=False)
	remarks = ndb.StringProperty(indexed=False)

class User(ndb.Model):
	name = ndb.StringProperty()
	email = ndb.StringProperty()
	level = ndb.IntegerProperty(indexed=False)
	# level 1 - mortal
	# level 2 - immortal admin