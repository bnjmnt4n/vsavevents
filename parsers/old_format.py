import logging
from datetime import date, time

from app.models import Event
from google.appengine.ext import ndb

def parse(msg):
    msg = msg.split('::: A USER HAS ENTERED A REQUEST FOR A AUDIO VISUAL WORK ORDER ::::')
    if len(msg) != 2:
        # decline all messages that aren't work orders
        logging.error("Message is not a valid work order. Disposing message.")
        return

    # split up the divider between info and equipment
    vals = msg[1].split('================================================')

    if len(vals) != 2: # decline all messages that aren't work orders
        return

    info = parse_info(vals[0], vals[1])
    logging.info(info)

    if info is None:
        return

    events_query = Event.query(
        ndb.AND(Event.name == info['name'], Event.date == info['date']),
        ndb.AND(Event.end_time == info['end_time'], Event.start_time == info['start_time'])
    )
    events_list = events_query.fetch()

    if len(events_list) == 0:
        Event(**info).put()

def parse_info(info, equipment):
    vals = [val for val in info.split('\n') if val.strip() != '' and val.find(': ') != -1]
    vals = [val.split(': ')[1] for val in vals]

    remarks = ''
    if len(vals) == 10:
        remarks = vals[9]

    vals = {
        'teacher': vals[0],
        'name': vals[1],
        'date': vals[3],
        'levels': vals[5],
        'location': vals[6],
        'start_time': vals[7],
        'end_time': vals[8],
        'remarks': remarks.strip()
    }

    # date
    d = vals['date'].split('/')
    vals['date'] = date(int(d[2]), int(d[1]), int(d[0]))

    # start and end times
    for val in ('start_time', 'end_time'):
        t = vals[val]
        vals[val] = time(int(t[0:2]), int(t[2:4]))

    vals['equipment'] = parse_equipment(equipment)

    return vals

def parse_equipment(lines):
    vals = [val for val in lines.split('\n') if val.strip() != '']

    # invalid input
    if vals[0].find('EQUIPMENT NEEDED:') == -1:
        return None
    else:
        remarks = vals[6:]
        vals = vals[1:6]

    new_vals = []
    vals = [val.split(', ')[0].split(': ')[1].strip() for val in vals]
    strs = ['Mic(s)', 'Rostrum', 'Spotlights', 'Projector', 'Mic Stand(s)']

    for i in range(0, len(vals)):
        string = ''
        val = vals[i]

        if val == 'Yes':
            val = True
        elif val == 'No':
            val = False
        else:
            try:
                val = int(val)
            except Exception:
                pass

        if val:
            if isinstance(val, int) and val is not True:
                string += str(val) + ' '
            string += strs[i]
            new_vals.append(string)

    remarks_str = "".join(remarks).strip("Remarks:").strip()
    remarks_str = "<br>" + "[" + remarks_str + "]" if remarks_str != "" else ""
    return ", ".join(new_vals) + remarks_str
