#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb

from utils import user, date, html, integers, template
from models import Event

EVENTS_QUERY = Event.gql("WHERE date >= DATE(:1) ORDER BY date ASC, start_time ASC, end_time ASC")
ARCHIVES_QUERY = Event.gql("WHERE date < DATE(:1) ORDER BY date DESC, start_time ASC, end_time ASC")

class EventsHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user.level < 1:
            html.handle_error(self.response, 403, "403 - Forbidden")
            return

    	events_query = EVENTS_QUERY.bind(date.get_date())
        limit = integers.to_integer(self.request.get('limit'), 20)

        event_list = events_query.fetch(limit)

        template.send(self.response, 'templates/events.html', {
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

        if curr_user.level < 1:
            html.handle_error(self.response, 403, "403 - Forbidden")
            return

    	events_query = ARCHIVES_QUERY.bind(date.get_date())
        limit = integers.to_integer(self.request.get('limit'), 20)

        event_list = events_query.fetch(limit)

        template.send(self.response, 'templates/events.html', {
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

        if curr_user.level < 1:
            html.handle_error(self.response, 403, "403 - Forbidden")
            return

        try:
            event = ndb.Key(urlsafe=key).get()

            template.send(self.response, 'templates/event.html', {
                'title': 'Event: ' + event.name,
                'logoutUrl': logoutUrl,
                'user': curr_user,
                'event': event
            })
        except:
            html.handle_error(self.response, 404, "404 - Not found")

class DutyRosterHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user.level < 1:
            html.handle_error(self.response, 403, "403 - Forbidden")
            return

        event = ndb.Key

        template.send(self.response, 'templates/dutyroster.html', {
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
