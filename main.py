#!/usr/bin/env python

import webapp2
import os
import jinja2

import users
from models import Event

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	template = JINJA_ENVIRONMENT.get_template('index.html')
    	user = users.get_user()
        loginUrl, logoutUrl = users.create_login_urls(self.request.path)

    	events_query = Event.query().order(-Event.date, Event.start_time, Event.end_time)
        event_list = events_query.fetch(10)
        
        self.response.out.write(template.render({
            'loginUrl': loginUrl,
            'logoutUrl': logoutUrl,
        	'user': user,
        	'events': event_list
        }))

app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
