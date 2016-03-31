#!/usr/bin/env python

import webapp2
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from app.models import User
from utils import user, template, html

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if not curr_user:
            # exit early if logged out
            template.send(self.response, 'logout.html', {
                'title': 'Home',
                'loginUrl': loginUrl,
                'user': None
            })
            return

        template.send(self.response, 'home.html', {
            'title': 'Home',
            'logoutUrl': logoutUrl,
            'user': curr_user
        })

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
