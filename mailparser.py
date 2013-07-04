import logging
from datetime import date, time

from models import Event
from google.appengine.ext import ndb

def parse(message):
	# parse special cases here

	msg = message.split('::: A USER HAS ENTERED A REQUEST FOR A AUDIO VISUAL WORK ORDER ::::')
	if len(msg) != 2: # decline all messages that aren't work orders
		return

	# split up the divider between info and equipment
	vals = msg[1].split('================================================')
	
	if len(vals) != 2: # decline all messages that aren't work orders
		return
	
	info = parse_info(vals[0], vals[1])
	logging.info(info)
	
	if info == None:
		return
	
	events_query = Event.query(
		ndb.AND(Event.name == info['name'], Event.date == info['date']),
		ndb.AND(Event.end_time == info['end_time'], Event.start_time == info['start_time'])
	)
	events_list = events_query.fetch()

	if len(events_list) == 0:
		Event(**info).put()

def parse_info(info, equipment):
	vals = info.split('\n')
	vals = [val for val in vals if val.strip() != '' and val.find(': ') != -1]

	new_vals = {}

	vals = [val.split(': ')[1] for val in vals]

	vals = {
		'teacher': vals[0],
		'name': vals[1],
		'department': vals[2],
		'date': vals[3],
		'levels': vals[5],
		'location': vals[6],
		'start_time': vals[7],
		'end_time': vals[8]
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
	vals = lines.split('\n')
	vals = [val for val in vals if val.strip() != '']

	# invalid input
	if vals[0].find('EQUIPMENT NEEDED:') == -1:
		return None
	else:
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
			except Exception, e:
				pass

		if val:
			if isinstance(val, int) and val is not True:
				string += str(val) + ' '
			string += strs[i]
			new_vals.append(string)

	return ", ".join(new_vals)
