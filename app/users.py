#!/usr/bin/env python

import webapp2, re
from google.appengine.ext import ndb

from app.models import User
from utils import template, integers

USERS_QUERY = User.gql("ORDER BY level DESC, name ASC, email ASC")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class UsersListHandler(webapp2.RequestHandler):
    def get(self):
        template.send(self, 'users.html', {
            'title': 'Users',
            'users': USERS_QUERY.fetch(),
        })

class UserHandler(webapp2.RequestHandler):
    def get(self, key):
        viewed_user = ndb.Key(urlsafe=key).get()
        template.send(self, 'user.html', {
            'title': 'User: ' + viewed_user.name,
            'viewed_user': viewed_user
        })
    def post(self, key):
        viewed_user = ndb.Key(urlsafe=key).get()

        if self.request.get('delete') == 'delete':
            viewed_user.key.delete()
            self.redirect('/users')
            return

        viewed_user.name = self.request.get('name') or 'Unknown'
        viewed_user.email = self.request.get('email')
        viewed_user.level = integers.to_integer(self.request.get('level'), 1)

        if not EMAIL_REGEX.match(viewed_user.email):
            template.send(self, 'user.html', {
                'title': 'User: ' + viewed_user.name,
                'viewed_user': viewed_user,
                'message': 'Please enter a valid email address.'
            })
            return

        viewed_user.put()

        template.send(self, 'user.html', {
            'title': 'User: ' + viewed_user.name,
            'viewed_user': viewed_user
        })

class NewUserHandler(webapp2.RequestHandler):
    def get(self):
        template.send(self, 'user.html', {
            'title': 'New User',
            'viewed_user': {
                'new': True
            }
        })
    def post(self):
        info = {
            'name': self.request.get('name') or 'Unknown',
            'email': self.request.get('email'),
            'level': integers.to_integer(self.request.get('level'), 1)
        }

        if not EMAIL_REGEX.match(info['email']):
            info['new'] = True
            template.send(self, 'user.html', {
                'title': 'New User',
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
