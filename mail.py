import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import parser

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        message = mail_message.bodies('text/plain')
        parser.parse(message)
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
