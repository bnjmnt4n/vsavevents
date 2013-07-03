import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import mailparser

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("%s: %s" % (mail_message.sender, mail_message.subject))
        plaintext = mail_message.bodies('text/plain')
        
        for text in plaintext:
            txtmsg = ""
            txtmsg = text[1].decode()
            logging.info(txtmsg)
            mailparser.parse(txtmsg)
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
