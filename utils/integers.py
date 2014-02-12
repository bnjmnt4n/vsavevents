def to_integer(string, default):
	limit = string

	try:
		limit = int(limit)
	except:
		limit = default

	return limit
