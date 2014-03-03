# [vsavevents](https://vsavevents.appspot.com) [![Build Status](http://b.adge.me/travis/d10/vsavevents.svg)](https://travis-ci.org/d10/vsavevents)

[vsavevents](https://vsavevents.appspot.com) is a parser and displayer for VS AV Club's work orders. <br>
It runs on Google's App Engine service, and is written in Python.

## Get started
Run the app in the launcher/via dev_appserver.py,
then send in the example data from the admin console as an email.

1. Install the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).
2. Start the local server using the Google App Engine SDK for Python.
3. Send in work orders to `events@vsavevents.appspot.com` through the admin console.

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
