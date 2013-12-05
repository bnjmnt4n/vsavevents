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

class Admin_AddUserHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name')
        email = self.request.get('email')
        level = int(self.request.get('level'))

        self.response.headers['Content-Type'] = 'text/plain'

        curr_user = user.get_user()
        if curr_user and curr_user.level < 2:
            template = JINJA_ENVIRONMENT.get_template('templates/admin/forbidden.txt')
            self.response.out.write(template.render())
            return

        q = User.query(User.email == email)
        adduser = q.get()
        if adduser:
            template = JINJA_ENVIRONMENT.get_template('templates/admin/adduser/exists.txt')
            self.response.out.write(template.render({
                'name': name,
                'email': email,
                'level': level
            }))
            return

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
        email = self.request.get('email')

        self.response.headers['Content-Type'] = 'text/plain'

        curr_user = user.get_user()
        if curr_user and curr_user.level < 2:
            template = JINJA_ENVIRONMENT.get_template('templates/admin/forbidden.txt')
            self.response.out.write(template.render())
            return

        q = User.query(User.email == email)
        rmuser = q.get()
        if not rmuser:
            template = JINJA_ENVIRONMENT.get_template('templates/admin/rmuser/notexists.txt')
            self.response.out.write(template.render({
                'email': email
            }))
            return

        template = JINJA_ENVIRONMENT.get_template('templates/admin/rmuser/success.txt')
        self.response.out.write(template.render({
            'name': rmuser.name,
            'email': email,
            'level': rmuser.level
        }))

        rmuser.key.delete()

app = webapp2.WSGIApplication([
    ('/admin/adduser.*', Admin_AddUserHandler),
    ('/admin/rmuser.*', Admin_RmUserHandler)
], debug=True)