#!/usr/bin/env python

import webapp2
import os
import jinja2
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from models import User
from utils import user

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if not curr_user:
        # logged out
            template = JINJA_ENVIRONMENT.get_template('templates/loggedout.html')
            self.response.out.write(template.render({
                'title': 'Home',
                'loginUrl': loginUrl,
                'user': None
            }))
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/home.html')
            self.response.out.write(template.render({
                'title': 'Home',
                'logoutUrl': logoutUrl,
                'user': None
            }))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
