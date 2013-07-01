import logging
import webapp2
from google.appengine.api import mail

import parser

class EmailHandler(webapp2.RequestHandler):
	def post(self):
		message = mail.InboundEmailMessage(self.request.body)

		# get text/plain
		content = list(message.bodies())[1][1].decode()
		logging.info(content)
		parser.parse(content)

app = webapp2.WSGIApplication([
	('/_ah/mail/.+', EmailHandler)
], debug=True)
