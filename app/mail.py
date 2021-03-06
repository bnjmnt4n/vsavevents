import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from parsers import old_format, new_format

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        sender = mail_message.sender
        subject = mail_message.subject

        if "<" in sender and ">" in sender:
            sender = sender.split("<")[1].split(">")[0]

        logging.info("%s: %s" % (sender, subject))

        text_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        if sender in (
                "vsavict@gmail.com",
                "victoriaschoolavclub@gmail.com",
                "demoneaux@gmail.com",
                "weien1292@gmail.com",
                "wei2912.supp0rt@gmail.com",
                "webmaster@vs.moe.edu.sg"
        ):
            if "[WORK ORDER]" in subject:
                for text in html_bodies:
                    txt = text[1].decode()
                    logging.info(txt)
                    new_format.parse(txt)
            elif "Audio Visual Department - Work Order Form" in subject:
                for text in text_bodies:
                    txt = text[1].decode()
                    logging.info(txt)
                    old_format.parse(txt)

app = webapp2.WSGIApplication([
    LogSenderHandler.mapping()
], debug=True)
