from datetime import datetime, timedelta

def getdate():
	return str((datetime.now() + timedelta(0, 0, 0, 0, 0, 8)).date())
