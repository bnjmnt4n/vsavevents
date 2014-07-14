#!/usr/bin/env python

import webapp2, re
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from app.models import User
from utils import user, template

class Admin(webapp2.RequestHandler):
    def get(self):
        curr_user = user.get_user()
        loginUrl, logoutUrl = user.create_login_urls(self.request.path)

        template.send(self.response, 'admin.html', {
            'title': 'Admin Panel',
            'logoutUrl': logoutUrl,
            'user': curr_user
        })

class Admin_ConsoleInput(webapp2.RequestHandler):
    def get(self):
        cmd = self.request.get('cmd').strip()

        i = 0
        template_data = None
        while not template_data:
            if i == 0:
                template_data = self.adduser(cmd)
            elif i == 1:
                template_data = self.rmuser(cmd)
            elif i == 2:
                template_data = self.finduser(cmd)
            elif i == 3:
                template_data = self.help(cmd)
            else:
                template_data = template.render('console/invalid.txt', {})
            i += 1
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(template_data)
    
    re_adduser = re.compile(r'adduser\s+(?:(\w+)|\"(.+?)\")\s+([^\s]+?@\w+\.com)\s+([12])')
    def adduser(self, cmd):
        m = self.re_adduser.match(cmd)
        if not m:
            return None
        
        groups = [x for x in m.groups() if x] # remove all None objects
        name = groups[0]
        email = groups[1]
        level = int(groups[2])

        adduser = User.query(User.email == email).get()
        if adduser: # user already exists
            return template.render('console/adduser/exists.txt', {
                'name': User.name,
                'email': User.email,
                'level': User.level
            })

        # create new user
        adduser = User(name=name, email=email, level=level)
        adduser.put()

        return template.render('console/adduser/success.txt', {
            'name': name,
            'email': email,
            'level': level
        })

    re_rmuser = re.compile(r'rmuser\s+([^\s]+?@\w+\.com)')
    def rmuser(self, cmd):
        m = self.re_rmuser.match(cmd)
        if not m:
            return None

        email = m.groups()[0]
        rmuser = User.query(User.email == email).get()
        if not rmuser: # user does not exist
        	return template.render('console/rmuser/notexists.txt', {
                'email': email
            })

        # create new user
        name = rmuser.name
        level = rmuser.level

        rmuser.key.delete()

    	return template.render('console/rmuser/success.txt', {
            'name': name,
            'email': email,
            'level': level
        })

    re_finduser = re.compile(r'finduser\s+([^\s]+?@\w+\.com)')
    def finduser(self, cmd):
        m = self.re_finduser.match(cmd)
        if not m:
            return None

        email = m.groups()[0]
        user = User.query(User.email == email).get()
        if not user: # user does not exist
            return template.render('console/finduser/notexists.txt', {
                'email': email
            })

        return template.render('console/finduser/success.txt', {
            'name': user.name,
            'email': user.email,
            'level': user.level
        })

    re_help = re.compile(r'help(?:\s+(\w+))?')
    def help(self, cmd):
        m = self.re_help.match(cmd)
        if not m:
            return None

        groups = m.groups()
        if not groups[0]:
            return template.render('console/help.txt', {})
        else:
            help_cmd = groups[0]
            if help_cmd == "adduser":
                return template.render('console/help/adduser.txt', {})
            elif help_cmd == "rmuser":
                return template.render('console/help/rmuser.txt', {})
            elif help_cmd == "finduser":
                return template.render('console/help/finduser.txt', {})

class Admin_AnnounceInput(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('text').strip()
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(template_data)

app = webapp2.WSGIApplication([
    ('/admin', Admin),
    ('/admin/console*', Admin_ConsoleInput),
    ('/admin/email*', Admin_AnnounceInput)
], debug=True)
