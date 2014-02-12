#!/usr/bin/env python

import webapp2
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from models import User
from utils import user, template

class Admin_Console(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        template.send(self.response, 'templates/admin.html', {
            'title': 'Admin Console',
            'logoutUrl': logoutUrl,
            'user': curr_user
        })

class Admin_AddUserHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        name = self.request.get('name')
        email = self.request.get('email')
        level = int(self.request.get('level'))

        adduser = User.query(User.email == email).get()
        if adduser: # user already exists
            template.send(self.response, 'templates/admin/adduser/exists.txt', {
                'name': name,
                'email': email,
                'level': level
            })
            return

        # create new user
        adduser = User(name=name, email=email, level=level)
        adduser.put()

        template.send(self.response, 'templates/admin/adduser/success.txt', {
            'name': name,
            'email': email,
            'level': level
        })

class Admin_RmUserHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        email = self.request.get('email')

        rmuser = User.query(User.email == email).get()
        if not rmuser: # if user does not exist
            template.send(self.response, 'templates/admin/rmuser/notexists.txt', {
                'email': email
            })
            return

        name = rmuser.name
        level = rmuser.level

        # remove the user
        rmuser.key.delete()

        template.send(self.response, 'templates/admin/rmuser/success.txt', {
            'name': name,
            'email': email,
            'level': level
        })

app = webapp2.WSGIApplication([
    ('/admin', Admin_Console),
    ('/admin/adduser.*', Admin_AddUserHandler),
    ('/admin/rmuser.*', Admin_RmUserHandler)
], debug=True)
