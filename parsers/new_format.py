import logging
from datetime import date, time, datetime

from models import Event
from google.appengine.ext import ndb

from utils import html

def parse(msg):
    msg = html.strip_tags(msg)
    msg = msg.split('Dear AV/IT Dept, AV Teacher ICs, AV Club members,')
    if len(msg) != 2: 
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

    equipment = []

    if not microphones == "0" and not microphones == "":
        equipment.append(microphones + " microphones")
    if not microphone_stands == "0" and not microphone_stands == "":
        equipment.append(microphone_stands + " microphone stands")
    if rostrum == "Yes":
        equipment.append("Rostrum microphones")
    if spotlights == "Yes":
        equipment.append("Spotlights")
    if projector == "Yes":
        equipment.append("Projector")

    info['equipment'] = ", ".join(equipment)

    return info
