#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb

from utils import user, date, html, integers, template
from app.models import Event

EVENTS_QUERY = Event.gql("WHERE date >= DATE(:1) ORDER BY date ASC, start_time ASC, end_time ASC")
ARCHIVES_QUERY = Event.gql("WHERE date < DATE(:1) ORDER BY date DESC, start_time ASC, end_time ASC")

class EventsHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

    	events_query = EVENTS_QUERY.bind(date.get_date())
        limit = integers.to_integer(self.request.get('limit'), 20)

        event_list = events_query.fetch(limit)

	template.send(self.response, 'events.html', {
            'title': 'Events',
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'events': event_list,
            'url': 'events'
        })

class ArchivesHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

    	events_query = ARCHIVES_QUERY.bind(date.get_date())
        limit = integers.to_integer(self.request.get('limit'), 20)

        event_list = events_query.fetch(limit)
	template.send(self.response, 'events.html', {
            'title': 'Archives',
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'events': event_list,
            'url': 'archives'
        })

class EventHandler(webapp2.RequestHandler):
    def get(self, key):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        event = ndb.Key(urlsafe=key).get()
	template.send(self.response, 'event.html', {
            'title': 'Event: ' + event.name,
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'event': event
        })

class DutyRosterHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        event = ndb.Key
	template.send(self.response, 'dutyroster.html', {
            'title': 'Duty Roster',
            'logoutUrl': logoutUrl,
            'user': curr_user
        })

app = webapp2.WSGIApplication([
    ('/events', EventsHandler),
    ('/archives', ArchivesHandler),
    ('/events/(.+)', EventHandler),
    ('/dutyroster', DutyRosterHandler)
], debug=True)
