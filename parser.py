import logging
import datetime
import events
import re

def parse(message):
    vals = message.split('================================================')
    info = parse_info(vals[0])
    logging.info(info)
    events.Event(**info).put()

def parse_info(info):
	vals = info.split('\n')
	new_vals = []

	for val in vals:
		if val != '':
			new_vals.append(val)

	if new_vals[0].find('::: A USER HAS') != -1:
		return None

	vals = {
		'teacher': new_vals[1],
		'name': new_vals[2],
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

	return new_vals

def parse_equipment(str):
	vals = info.split('\n')
	new_vals = []

	for val in vals:
		if val != '':
			new_vals.append(val)

	#if new_vals[0]

