#!/usr/bin/env python

import webapp2
import os
import jinja2
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from utils import user, date
from models import Event

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

EVENTS_QUERY = Event.gql("WHERE date >= DATE(:1) ORDER BY date ASC, start_time ASC, end_time ASC")
ARCHIVES_QUERY = Event.gql("WHERE date < DATE(:1) ORDER BY date DESC, start_time ASC, end_time ASC")

def get_limit(request, default):
    limit = request.get('limit')
    try:
        limit = int(limit)
        return limit
    except:
        return default

def handle_error(response, status, message):
    response.write("<html><head><title>%s</title></head><body><h1>%s</h1></body></html>" % (message, message))
    response.set_status(status)

class EventsHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user.level < 1:
            handle_error(self.response, 403, "403 - Forbidden")
            return

    	events_query = EVENTS_QUERY.bind(date.getdate())
        limit = get_limit(self.request, 20)

        event_list = events_query.fetch(limit)

        template = JINJA_ENVIRONMENT.get_template('templates/events.html')
        self.response.out.write(template.render({
            'title': 'Events',
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'events': event_list
        }))

class ArchivesHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user.level < 1:
            handle_error(self.response, 403, "403 - Forbidden")
            return

    	events_query = ARCHIVES_QUERY.bind(date.getdate())
        limit = get_limit(self.request, 20)

        event_list = events_query.fetch(limit)

        template = JINJA_ENVIRONMENT.get_template('templates/events.html')
        self.response.out.write(template.render({
            'title': 'Archives',
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'events': event_list
        }))

class EventHandler(webapp2.RequestHandler):
    def get(self, key):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user.level < 1:
            handle_error(self.response, 403, "403 - Forbidden")
            return

        try:
            event = ndb.Key(urlsafe=key).get()

            template = JINJA_ENVIRONMENT.get_template('templates/event.html')
            self.response.out.write(template.render({
                'title': 'Event: ' + event.name,
                'logoutUrl': logoutUrl,
                'user': curr_user,
                'event': event
            }))
        except:
            handle_error(self.response, 404, "404 - Not found")

class DutyRosterHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user.level < 1:
            handle_error(self.response, 403, "403 - Forbidden")
            return

        event = ndb.Key

        template = JINJA_ENVIRONMENT.get_template('templates/dutyroster.html')
        self.response.out.write(template.render({
            'title': 'Duty Roster',
            'logoutUrl': logoutUrl,
            'user': curr_user
        }))

app = webapp2.WSGIApplication([
    ('/events', EventsHandler),
    ('/archives', ArchivesHandler),
    ('/events/(.+)', EventHandler),
    ('/dutyroster', DutyRosterHandler)
], debug=True)
