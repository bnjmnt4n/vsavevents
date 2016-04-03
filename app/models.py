from google.appengine.ext import ndb

class Event(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateProperty()
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()

    teacher = ndb.StringProperty()
    location = ndb.StringProperty()
    levels = ndb.StringProperty()
    equipment = ndb.StringProperty()
    remarks = ndb.StringProperty()

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    level = ndb.IntegerProperty()
