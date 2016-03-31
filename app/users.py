#!/usr/bin/env python

import webapp2, re
from google.appengine.ext import ndb

from app.models import User
from utils import user, template, integers

email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class UsersListHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        template.send(self.response, 'users.html', {
            'title': 'Users',
            'logoutUrl': logoutUrl,
            'users': User.query().order(-User.level, User.name, User.email),
            'user': curr_user
        })

class UserHandler(webapp2.RequestHandler):
    def get(self, key):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        viewed_user = ndb.Key(urlsafe=key).get()
        template.send(self.response, 'user.html', {
            'title': 'User: ' + viewed_user.name,
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'viewed_user': viewed_user
        })
    def post(self, key):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        viewed_user = ndb.Key(urlsafe=key).get()

        if self.request.get('delete') == 'delete':
            viewed_user.key.delete()
            self.redirect('/users')
            return

        viewed_user.name = self.request.get('name') or 'Unknown'
        viewed_user.email = self.request.get('email')
        viewed_user.level = integers.to_integer(self.request.get('level'), 1)

        if not email_regex.match(viewed_user.email):
            template.send(self.response, 'user.html', {
                'title': 'User: ' + viewed_user.name,
                'logoutUrl': logoutUrl,
                'user': curr_user,
                'viewed_user': viewed_user,
                'message': 'Please enter a valid email address.'
            })
            return

        viewed_user.put()

        template.send(self.response, 'user.html', {
            'title': 'User: ' + viewed_user.name,
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'viewed_user': viewed_user
        })

class NewUserHandler(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        template.send(self.response, 'user.html', {
            'title': 'New User',
            'logoutUrl': logoutUrl,
            'user': curr_user,
            'viewed_user': {
                'new': True
            }
        })
    def post(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        info = {
            'name': self.request.get('name') or 'Unknown',
            'email': self.request.get('email'),
            'level': integers.to_integer(self.request.get('level'), 1)
        }

        if not email_regex.match(info['email']):
            info['new'] = True
            template.send(self.response, 'user.html', {
                'title': 'New User',
                'logoutUrl': logoutUrl,
                'user': curr_user,
                'viewed_user': info,
                'message': 'Please enter a valid email address.'
            })
            return

        key = User(**info).put()

        self.redirect('/users/' + key.urlsafe())

app = webapp2.WSGIApplication([
    ('/users/?', UsersListHandler),
    ('/users/new', NewUserHandler),
    ('/users/(.+)', UserHandler),
], debug=True)
