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
    	template = JINJA_ENVIRONMENT.get_template('templates/events.html')
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

    	events_query = EVENTS_QUERY.bind(date.getdate())
        event_list = events_query.fetch(20)
        
        self.response.out.write(template.render({
            'title': 'Events',
            'loginUrl': loginUrl,
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'events': event_list
        }))

class ArchivesHandler(webapp2.RequestHandler):
    def get(self):
    	template = JINJA_ENVIRONMENT.get_template('templates/events.html')
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

    	events_query = ARCHIVES_QUERY.bind(date.getdate())
        event_list = events_query.fetch(10)
        
        self.response.out.write(template.render({
            'title': 'Archives',
            'loginUrl': loginUrl,
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'events': event_list
        }))

class EventHandler(webapp2.RequestHandler):
    def get(self, key):
        template = JINJA_ENVIRONMENT.get_template('templates/event.html')
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        event = ndb.Key(urlsafe=key).get()

        if event:
            self.response.out.write(template.render({
                'title': 'Event: ' + event.name,
                'loginUrl': loginUrl,
                'logoutUrl': logoutUrl,
                'user': curr_user,
                'event': event
            }))

app = webapp2.WSGIApplication(
	[('/', MainHandler),
	 ('/archives', ArchivesHandler),
     ('/events/(.*)', EventHandler)],
   debug=True)
