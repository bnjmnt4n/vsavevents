#!/usr/bin/env python

import webapp2
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from app.models import User
from utils import user, template

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if not curr_user:
        # logged out
            template.send(self.response, 'templates/loggedout.html', {
                'title': 'Home',
                'loginUrl': loginUrl,
                'user': None
            })
        else:
            template.send(self.response, 'templates/home.html', {
                'title': 'Home',
                'logoutUrl': logoutUrl,
                'user': None
            })

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
