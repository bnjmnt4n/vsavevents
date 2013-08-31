import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from parsers import old_format, new_format

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        sender = mail_message.sender
        subject = mail_message.subject

        logging.info("%s: %s" % (sender, subject))

        text_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        if sender in ("vsavict@gmail.com", "demoneaux@gmail.com", "weien1292@gmail.com"):
            for text in html_bodies:
                txt = text[1].decode()
                logging.info(txt)
                new_format.parse(txt)
        elif sender in ("webmaster@vs.moe.edu.sg"): # to be shifted to new format soon
            for text in text_bodies:
                txt = text[1].decode()
                logging.info(txt)
                old_format.parse(txt)
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
