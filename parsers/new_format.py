import logging
from datetime import date, time

from models import Event
from google.appengine.ext import ndb

import strip_html

def parse(msg):
  msg = strip_html.stript_tags(msg)
	info = parse(msg)
	logging.info(info)
	
	events_query = Event.query(
		ndb.AND(Event.name == info['name'], Event.date == info['date']),
		ndb.AND(Event.end_time == info['end_time'], Event.start_time == info['start_time'])
	)
	events_list = events_query.fetch()

	if len(events_list) == 0:
		Event(**info).put()

def parse(msg):
	vals = [val for val in info.split('\n') if val.strip() != '' and val.find(': ') != -1]
	vals = [val.split(': ')[1] for val in vals]

	remarks = ''
	if len(vals) == 10:
		remarks = vals[9]

	vals = {
		'teacher': vals[0],
		'name': vals[1],
		'department': vals[2],
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
