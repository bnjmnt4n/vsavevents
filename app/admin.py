#!/usr/bin/env python

import webapp2, re
from datetime import datetime, timedelta
from google.appengine.ext import ndb

from app.models import User
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
                template_data = template.render('templates/admin/invalid.txt', {})
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
            return template.render('templates/admin/adduser/exists.txt', {
                'name': User.name,
                'email': User.email,
                'level': User.level
            })

        # create new user
        adduser = User(name=name, email=email, level=level)
        adduser.put()

        return template.render('templates/admin/adduser/success.txt', {
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
            return template.render('templates/admin/rmuser/notexists.txt', {
                'email': email
            })

        # create new user
        name = rmuser.name
        level = rmuser.level

        rmuser.key.delete()

        return template.render('templates/admin/rmuser/success.txt', {
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
            return template.render('templates/admin/finduser/notexists.txt', {
                'email': email
            })

        return template.render('templates/admin/finduser/success.txt', {
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
            return template.render('templates/admin/help.txt', {})
        else:
            help_cmd = groups[0]
            if help_cmd == "adduser":
                return template.render('templates/admin/help/adduser.txt', {})
            elif help_cmd == "rmuser":
                return template.render('templates/admin/help/rmuser.txt', {})
            elif help_cmd == "finduser":
                return template.render('templates/admin/help/finduser.txt', {})

app = webapp2.WSGIApplication([
    ('/admin', Admin_Console),
    ('/admin/console*', Admin_ConsoleInput)
], debug=True)
