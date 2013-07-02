import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import mailparser

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        plaintext = mail_message.bodies('text/plain')
        
        for text in plaintext:
            txtmsg = ""
            txtmsg = text[1].decode()
            mailparser.parse(txtmsg)
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
