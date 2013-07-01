import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

import parser

class LogSenderHandler(InboundMailHandler):
	def receive(self, message):
		logging.info("Received a message from: " + message.sender)
		parser.parse(message.bodies('text/plain'))

app = webapp2.WSGIApplication([
	('/_ah/mail/.+', InboundMailHandler)
], debug=True)
