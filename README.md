# [vsavevents](https://vsavevents.appspot.com/) [![Build Status](https://travis-ci.org/d10/vsavevents.svg?branch=master)](https://travis-ci.org/d10/vsavevents)

[vsavevents](https://vsavevents.appspot.com/) is a parser and displayer for [Victoria School](http://vs.moe.edu.sg/) Audio-Visual Club’s work orders.  
It runs on [Google’s](https://www.google.com/) [App Engine](https://cloud.google.com/appengine) service, and is written in [Python](https://www.python.org/).

## Get started

1. Install the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).
2. Start a local server using the App Engine SDK.
3. To access the site, you need to add yourself as a user. Go to the console at [localhost:8000](http://localhost:8000/console) and execute the following, replacing the values with appropriate ones:

    ```python
    from app.models import User

    adduser = User(name="Test Example", email="test@example.com")
    adduser.put()
    ```
 
    Once your user is added, you may proceed to view the site. This is only required the first time to add an admin; from now on, you can use the Admin Console.

## Admin Console

A console is available at `/admin` for administrators only.
