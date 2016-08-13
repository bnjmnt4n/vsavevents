#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

from utils import date, integers, template
from app.models import Event

EVENTS_QUERY = Event.gql("WHERE date >= DATE(:1) ORDER BY date ASC, start_time ASC, end_time ASC")
ARCHIVES_QUERY = Event.gql("WHERE date < DATE(:1) ORDER BY date DESC, start_time ASC, end_time ASC")

class EventsHandler(webapp2.RequestHandler):
    def get(self):
    	events_query = EVENTS_QUERY.bind(date.get_date())

        cursor = Cursor(urlsafe=self.request.get('cursor'))
        events, next_cursor, more = events_query.fetch_page(25, start_cursor=cursor)

        next_link = None
        if more and next_cursor:
            next_link = next_cursor.urlsafe()

        template.send(self, 'events.html', {
            'title': 'Events',
            'events': events,
            'url': 'events',
            'next': next_link
        })

class ArchivesHandler(webapp2.RequestHandler):
    def get(self):
    	events_query = ARCHIVES_QUERY.bind(date.get_date())

        cursor = Cursor(urlsafe=self.request.get('cursor'))
        events, next_cursor, more = events_query.fetch_page(25, start_cursor=cursor)

        next_link = None
        if more and next_cursor:
            next_link = next_cursor.urlsafe()

        template.send(self, 'events.html', {
            'title': 'Archives',
            'events': events,
            'url': 'archives',
            'next': next_link
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
