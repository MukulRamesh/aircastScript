from contextlib import redirect_stdout

f = open('LOG.txt', 'w')
with redirect_stdout(f):
	import unzip
	import cleanup

# This file is what should be run to start the utility.