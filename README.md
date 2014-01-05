# [vsavevents](https://vsavevents.appspot.com) [![Build Status](https://travis-ci.org/d10/vsavevents.png)](https://travis-ci.org/d10/vsavevents)

[vsavevents](https://vsavevents.appspot.com) is a work order parser and displayer

## Get started
Run the app in the launcher/via dev_appserver.py,
then send in the example data from the admin console as an email.

## Admin API

### adduser

	/admin/adduser?name=NAME&email=EMAIL&level=LEVEL

Adds user to database.

Level must be an integer. Here are the following levels:

	1 - Normal
	2 - Administrator

### rmuser

	/admin/rmuser?email=EMAIL

Remove user from database.