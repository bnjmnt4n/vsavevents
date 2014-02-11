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

class Admin_Console(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        template = JINJA_ENVIRONMENT.get_template('templates/admin.html')
        self.response.out.write(template.render({
            'title': 'Admin Console',
            'logoutUrl': logoutUrl,
            'user': curr_user
        }))

class Admin_AddUserHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        name = self.request.get('name')
        email = self.request.get('email')
        level = int(self.request.get('level'))

        adduser = User.query(User.email == email).get()
        if adduser: # user already exists
            template = JINJA_ENVIRONMENT.get_template('templates/admin/adduser/exists.txt')
            self.response.out.write(template.render({
                'name': name,
                'email': email,
                'level': level
            }))
            return

        # create new user
        adduser = User(name=name, email=email, level=level)
        adduser.put()

        template = JINJA_ENVIRONMENT.get_template('templates/admin/adduser/success.txt')
        self.response.out.write(template.render({
            'name': name,
            'email': email,
            'level': level
        }))

class Admin_RmUserHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        email = self.request.get('email')

        rmuser = User.query(User.email == email).get()
        if not rmuser: # if user does not exist
            template = JINJA_ENVIRONMENT.get_template('templates/admin/rmuser/notexists.txt')
            self.response.out.write(template.render({
                'email': email
            }))
            return

        name = rmuser.name
        level = rmuser.level

        # remove the user
        rmuser.key.delete()

        template = JINJA_ENVIRONMENT.get_template('templates/admin/rmuser/success.txt')
        self.response.out.write(template.render({
            'name': name,
            'email': email,
            'level': level
        }))

app = webapp2.WSGIApplication([
    ('/admin', Admin_Console),
    ('/admin/adduser.*', Admin_AddUserHandler),
    ('/admin/rmuser.*', Admin_RmUserHandler)
], debug=True)