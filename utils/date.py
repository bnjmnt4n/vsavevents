from datetime import datetime, timedelta

def get_date():
	return str((datetime.now() + timedelta(0, 0, 0, 0, 0, 8)).date())
