#!/usr/bin/env python

import webapp2

from utils import user, template

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        if not curr_user:
            # exit early if logged out
            template.send(self, 'logout.html', {
                'title': 'Home',
                'loginUrl': loginUrl,
                'user': None
            })
            return

        template.send(self, 'home.html', {
            'title': 'Home'
        })

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
