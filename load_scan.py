
import os
import time
import getopt
import sys

def do_scan():
	t = time.localtime()
	f = open(time.strftime("%Y%m%d.log", t), "a")

	print >> f, "+++++++++++++++++++++++++++++++"
	print >> f, "Time:", time.strftime("%Y-%m-%d %H:%M:%S", t)

	commands = (
		"top -c -n 1",
		"iostat",
		"./bin/ifstat",
		#"./bin/nethogs -t -c 1",
	)
	for cmd in commands:
		cmd = cmd + ' | sed -r "s/\\x1B\\[((\?)?[0-9]{1,2}(;[0-9]{1,2})?)?[mGKHhJc]//g"'
		print >> f, os.popen(cmd).read().decode('unicode-escape')
		print >> f, "\n----\n"

def load_scan(is_test):
	last_hour = -1
	while True:
		time.sleep(0.02)
		t = time.localtime()
		scan = False
		hour = t.tm_hour
		minute = t.tm_min
		if hour == 3 and minute in (0, 1):
			scan = True
		elif hour != last_hour:
			scan = True
		elif is_test:
			scan = True
		if scan:
			last_hour = hour
			do_scan()

if __name__ == "__main__":
	try:
		opts,args = getopt.getopt(sys.argv[1:], "t", [])
	except getopt.GetoptError:
		print "err exit."
		exit()
	is_test = False
	for o, a in opts:
		if o == "-t":
			is_test = True

	load_scan(is_test)


