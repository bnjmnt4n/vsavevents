#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb

from utils import date, integers, template
from app.models import Event

EVENTS_QUERY = Event.gql("WHERE date >= DATE(:1) ORDER BY date ASC, start_time ASC, end_time ASC")
ARCHIVES_QUERY = Event.gql("WHERE date < DATE(:1) ORDER BY date DESC, start_time ASC, end_time ASC")

class EventsHandler(webapp2.RequestHandler):
    def get(self):
    	events_query = EVENTS_QUERY.bind(date.get_date())
        limit = integers.to_integer(self.request.get('limit'), 20)

        event_list = events_query.fetch(limit)

        template.send(self, 'events.html', {
            'title': 'Events',
            'events': event_list,
            'url': 'events'
        })

class ArchivesHandler(webapp2.RequestHandler):
    def get(self):
    	events_query = ARCHIVES_QUERY.bind(date.get_date())
        limit = integers.to_integer(self.request.get('limit'), 20)

        event_list = events_query.fetch(limit)
        template.send(self, 'events.html', {
            'title': 'Archives',
            'events': event_list,
            'url': 'archives'
        })

class EventHandler(webapp2.RequestHandler):
    def get(self, key):
        event = ndb.Key(urlsafe=key).get()
        template.send(self, 'event.html', {
            'title': 'Event: ' + event.name,
            'event': event
        })

app = webapp2.WSGIApplication([
    ('/events', EventsHandler),
    ('/archives', ArchivesHandler),
    ('/events/(.+)', EventHandler)
], debug=True)
