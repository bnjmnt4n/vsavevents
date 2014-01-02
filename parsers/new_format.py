import logging
from datetime import date, time, datetime
import dateutil.parser

from models import Event
from google.appengine.ext import ndb

from utils import html

def parse(msg):
    msg = html.strip_tags(msg).split("\n")
    msg = [i.strip() for i in msg]
    for i in range(len(msg)):
        if msg[i][-1:] == ":":
            msg[i] = msg[i] + " " # add a space to the colon; dirty hack
    msg = '\n'.join(msg)
    msg = msg.split('Dear AV/IT Dept, AV Teacher ICs, AV Club members,')
    if len(msg) != 2: 
        # decline all messages that aren't work orders
        logging.error("Message is not a valid work order. Disposing message.")
        return
    
    msg = msg[1].split('-----------------------------------------------------------------------------------------------------------------------')
    
    logging.info(msg[0])
    
    info = parse_info(msg[0])
    logging.info(info)
    add_info(info)
    for i in range(1, 2): # there are 2 subsets
        subset = parse_subset(i+1, info, msg[i])
        add_info(subset)

def add_info(info):
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
    
    # strip all keys

    info = {
        'teacher': vals["Name"],
        'name': vals["Event"],
        'date': vals["Date of Event /Rehearsal"],
        'levels': vals["Level Involved"],
        'location': vals["Venue"],
        'start_time': vals["Actual Start Time"],
        'end_time': vals["End Time"],
        'remarks': msg.split("Any other remarks / instructions?: ")[1].replace("\n", "<br>"),
        'equipment': ""
    }

    # date
    info['date'] = dateutil.parser.parse(info['date']).date()

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

def parse_subset(i, info, msg):
    vals = [val for val in msg.split('\n') if val.strip() != '' and val.find(': ') != -1]
    vals = dict(val.split(": ") for val in vals)

    subset = {
        'teacher': info['teacher'],
        'name': info['name'] + " [%d]" % (i),
        'date': vals["[%d] Date of Event / Rehearsal" % (i)],
        'levels': info['levels'],
        'location': vals["[%d] Venue" % (i)],
        'start_time': vals["[%d] Actual Start Time" % (i)],
        'end_time': vals["[%d] End Time" % (i)],
        'remarks': info['remarks'],
        'equipment': ""
    }

    # date
    subset['date'] += " "
    subset['date'] += str(date.today().year)
    subset['date'] = datetime.strptime(subset['date'], "%b %d %Y").date()

    # start and end times
    for val in ('start_time', 'end_time'):
        subset[val] = datetime.strptime(subset[val], "%I:%M %p").time()

    # equipment
    microphones = vals["[%d] Microphones" % (i)]
    microphone_stands = vals["[%d] Microphone stands" % (i)]
    rostrum = vals["[%d] Rostrum Microphone" % (i)]
    spotlights = vals["[%d] Spot Lights for Performance" % (i)]
    projector = vals["[%d] Projector" % (i)]

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

    subset['equipment'] = ", ".join(equipment)

    return subset
