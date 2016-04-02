def to_integer(string, default):
	integer = string

	try:
		integer = int(integer)
	except:
		integer = default

	return integer
