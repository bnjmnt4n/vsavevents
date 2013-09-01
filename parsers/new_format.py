import logging
from datetime import date, time, datetime

from models import Event
from google.appengine.ext import ndb

import re

def parse(msg):
    msg = re.sub('<[^<]+?>', '', msg)
    
    if msg.find('Dear AV/IT Dept, AV Teacher ICs, AV Club members,') == -1: 
        # decline all messages that aren't work orders
        logging.error("Message is not a valid work order. Disposing message.")
        return
    
    info = parse_info(msg)
    logging.info(info)
    
    events_query = Event.query(
        ndb.AND(Event.name == info['name'], Event.date == info['date']),
        ndb.AND(Event.end_time == info['end_time'], Event.start_time == info['start_time'])
    )
    events_list = events_query.fetch()

    if not len(events_list) == 0:
        for val in events_list:
            val.key.delete()
    Event(**info).put()

def parse_info(msg):
    vals = [val for val in msg.split('\n') if val.strip() != '' and val.find(': ') != -1]
    vals = dict(val.split(": ") for val in vals)

    info = {
        'teacher': vals["Name"],
        'name': vals["Event"],
        'date': vals["Date of Event /Rehearsal"],
        'levels': vals["Level Involved"],
        'location': vals["Venue"],
        'start_time': vals["Actual Start Time"],
        'end_time': vals["End Time"],
        'remarks': vals["Any other remarks / instructions?"],
        'equipment': ""
    }

    # date
    info['date'] += " "
    info['date'] += str(date.today().year)
    info['date'] = datetime.strptime(info['date'], "%b %d %Y").date()

    # start and end times
    for val in ('start_time', 'end_time'):
        info[val] = datetime.strptime(info[val], "%I:%M %p").time()

    # equipment
    microphones = vals["Microphones"]
    microphone_stands = vals["Microphone stands"]
    rostrum = vals["Rostrum Microphone"]
    spotlights = vals["Spot Lights for Performance"]
    projector = vals["Projector"]

    if not microphones == "0" and not microphones == "":
        info['equipment'] += microphones
        info['equipment'] += " microphones <br>"
    if not microphone_stands == "0" and not microphone_stands == "":
        info['equipment'] += microphone_stands
        info['equipment'] += " microphone stands <br>"
    if rostrum == "Yes":
        info['equipment'] += "Rostrum microphones <br>"
    if spotlights == "Yes":
        info['equipment'] += "Spotlights <br>"
    if projector == "Yes":
        info['equipment'] += "Projector <br>"

    #vals['equipment'] = parse_equipment(equipment)

    return info
