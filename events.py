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

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user and curr_user.level < 1:
        # unauthorized
            template = JINJA_ENVIRONMENT.get_template('templates/forbidden.html')
            self.response.out.write(template.render({
                'title': 'Access Denied',
                'logoutUrl': logoutUrl,
                'user': curr_user
            }))
            return
        elif not curr_user:
        # logged out
            template = JINJA_ENVIRONMENT.get_template('templates/loggedout.html')
            self.response.out.write(template.render({
                'title': 'Home',
                'loginUrl': loginUrl,
                'user': None
            }))
            return

    	events_query = EVENTS_QUERY.bind(date.getdate())

        limit = self.request.get('limit')
        try:
            limit = int(limit)
        except:
            limit = events_query.count()

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

        if curr_user and curr_user.level < 1 or not curr_user:
            self.redirect("/")
            return

    	events_query = ARCHIVES_QUERY.bind(date.getdate())

        limit = self.request.get('limit')
        try:
            limit = int(limit)
        except:
            limit = events_query.count()

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

        if curr_user and curr_user.level < 1 or not curr_user:
            self.redirect("/")
            return

        event = ndb.Key(urlsafe=key).get()

        if event:
            template = JINJA_ENVIRONMENT.get_template('templates/event.html')
            self.response.out.write(template.render({
                'title': 'Event: ' + event.name,
                'logoutUrl': logoutUrl,
                'user': curr_user,
                'event': event
            }))

class DutyRosterHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user and curr_user.level < 1 or not curr_user:
            self.redirect("/")
            return

        template = JINJA_ENVIRONMENT.get_template('templates/dutyroster.html')
        self.response.out.write(template.render({
            'title': 'Duty Roster',
            'logoutUrl': logoutUrl,
            'user': curr_user
        }))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/archives', ArchivesHandler),
    ('/events/(.*)', EventHandler),
    ('/dutyroster', DutyRosterHandler)
], debug=True)
