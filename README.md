# [vsavevents](https://vsavevents.appspot.com) [![Build Status](http://b.adge.me/travis/d10/vsavevents.svg)](https://travis-ci.org/d10/vsavevents)

[vsavevents](https://vsavevents.appspot.com) is a parser and displayer for VS AV Club's work orders. <br>
It runs on Google's App Engine service, and is written in Python.

## Get started

Run the app in the launcher/via dev_appserver.py,
then send in the example data from the admin console as an email.

1. Install the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).
2. Start the local server using the Google App Engine SDK for Python.
3. To access the site, you need to add yourself as a user. Go to the console at [localhost:8000][localhost:8000/console] and type in the following:

	from app.models import User

	adduser = User(name="Test Example", email="test@example.com")
	adduser.put()

Replace the values accordingly.

When you are finished, press "Execute". Once your user is added, you may proceed to view the site. This is only required the first time to add an admin; from now on, you can use the Admin Console.

## Admin Console

A console is available at /admin for administrators only.