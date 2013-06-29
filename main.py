#!/usr/bin/env python

import webapp2
import os
import jinja2

import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	if users.verify_access():
    		self.response.write('Valid user')
    	# template = JINJA_ENVIRONMENT
        # self.response.write(template.render({}))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
