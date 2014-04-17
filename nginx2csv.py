# convert nginx-style logfile to csv with some janky regex
# James Dietrich - https://github.com/jbdietrich

import csv
import re
import sys

LOG_REGEX = r':([\d\.]+).*?\[(\d+\/\w+\/\d{4}):([\d{2}:]+).*"(\w{3,4})\s\/(\S+).*?(\d{3})\s\d+\s"\S+"\s"(.*?)"\s.*?"([\d\.]+)"'
COLUMNS = ('ip', 'date', 'time', 'method', 'path', 'status', 'user-agent', 'response-time')

def extractLogEntries(logFile):

	rows = []

	with open(logFile, 'rt') as f:
		raw = f.read()
		matches = re.findall(LOG_REGEX, raw)
		for match in matches:
			rows.append(match)

	return rows

def writeToCSV(csvFile, rows):

	with open(csvFile, 'wt') as f:
		writer = csv.writer(f)
		writer.writerow(COLUMNS)
		for row in rows:
			writer.writerow(row)

if __name__ == "__main__":

	try:
		rows = extractLogEntries(sys.argv[1])
		writeToCSV(sys.argv[2], rows)
	except IndexError:
		print "Please provide a logfile and a csv output file.\n" \
					"usage: python nginx2csv.py logfile.input output.csv"
