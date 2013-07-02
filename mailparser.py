import logging
import datetime
import events
import re
from google.appengine.ext import ndb

def parse(message):
	vals = message.split('================================================') # split up the divider between info and equipment
	
	info = parse_info(vals[0], vals[1])
	logging.info(info)
	
	events_query = events.Event.query(events.Event.name == info['name'])
	events_list = events_query.fetch()
	if len(events_list) == 0:
		events.Event(**info).put()

def parse_info(info, equipment):
	vals = info.split('\n')
	new_vals = []

	for val in vals:
		if val != '':
			new_vals.append(val)

	# invalid input
	if new_vals[0].find('::: A USER HAS') == -1:
		return None

	vals = {
		'teacher': new_vals[1],
		'name': new_vals[2],
		'department': new_vals[3],
		'date': new_vals[4],
		'levels': new_vals[6],
		'location': new_vals[7],
		'start_time': new_vals[8],
		'end_time': new_vals[9]
	}

	new_vals = {}

	for val in vals: 
		value = vals[val].split(': ')[1]
		new_vals[val] = value

	d = new_vals['date'].split('/')
	new_vals['date'] = datetime.date(int(d[2]), int(d[1]), int(d[0]))

	for val in ['start_time', 'end_time']:
		t = new_vals[val]
		new_vals[val] = datetime.time(int(t[0:2]), int(t[2:4]))

	new_vals['equipment'] = parse_equipment(equipment)

	return new_vals

def parse_equipment(line):
	vals = line.split('\n')
	new_vals = []

	for val in vals:
		if val != '' and val.find("EQUIPMENT NEEDED: ") == -1:
			new_vals.append(val)

	for i in range(0, len(new_vals)): 
		val = new_vals[i]
		if val.find(',    Purpose') == -1:
			continue
		new_vals[i] = val.split(',    Purpose')[0]
		
	return "<br>".join(new_vals)

