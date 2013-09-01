#!/usr/bin/env python

import webapp2
import os
import jinja2
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from utils import user, date
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class UsersHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if curr_user and not user.is_authorized(curr_user):
            template = JINJA_ENVIRONMENT.get_template('templates/forbidden.html')
            self.response.out.write(template.render({
                'title': 'Access Denied',
                'loginUrl': loginUrl,
                'logoutUrl': logoutUrl,
                'user': curr_user
            }))
            return

    	users_query = EVENTS_QUERY.bind(date.getdate())
        users_list = events_query.fetch(100) # get all users
        
        template = JINJA_ENVIRONMENT.get_template('templates/users.html')
        self.response.out.write(template.render({
            'title': 'Users',
            'loginUrl': loginUrl,
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'users': users_list
        }))

app = webapp2.WSGIApplication(
	[('/users', UsersHandler),
	 ('/users/(.*)', UserHandler),
     ('/users/(.*)/edit', EditHandler)
     ('/users/(.*)/delete', DeleteHandler)],
   debug=True)
