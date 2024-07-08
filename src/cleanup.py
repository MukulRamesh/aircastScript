import os, shutil
from os import listdir
import csv
import datetime
import graphing

DIR = "./temp/"

PERIOD = datetime.timedelta(days=14) # The last x amount of time that I am extracting

TICKER = datetime.timedelta(hours=1) # How the data is delineated: average by x amount of time

# Hard coded field names because the CSV file is badly formatted
fieldNames = ['ObjectID', 'Session_Name', 'Timestamp', 'Latitude', 'Longitude', 'Fahrenheit', 'PM1', 'PM10', 'PM2.5', '3-RH']

def hourlyAverage(fp):
	
	file = csv.DictReader(fp, delimiter=',', quotechar="'", fieldnames=fieldNames)
	lis = []

	for line in file:
		# timeVal = (time.strptime(line['Timestamp'], "%Y-%m-%dT%H:%M:%S.000"))
		timeVal = datetime.datetime.fromisoformat(line['Timestamp'])

		lis.append((timeVal, line['PM2.5'])) # Extracting the PM2.5


	mostRecentStamp = lis[-1][0]
	earliestStamp = mostRecentStamp - PERIOD

	periodData = []


	curStamp = mostRecentStamp
	i = -1
	while curStamp > earliestStamp:
		periodData.append(lis[i])
		
		i = i - 1
		curStamp = lis[i][0]
	
	periodData.reverse()
	
	averagedList = []
	i = 0
	ppmSum = 0
	obsCount = 0
	while i < len(periodData):
		
		markedStamp = periodData[i][0]
		endOfTicker = periodData[i][0] + TICKER

		curStamp = markedStamp
		while curStamp < endOfTicker and i < len(periodData):
			curStamp = periodData[i][0]
			
			if (periodData[i][1] != ''):
				ppmSum += float(periodData[i][1])
				obsCount += 1

			i = i + 1
		

		averagePPM = ppmSum / obsCount
		averagedList.append((markedStamp, averagePPM))
	
	return averagedList
		

def makeCleanGraph():
	entries = listdir(DIR)
	# print(entries)

	for entry in entries: # I assume that every zip file has only one point of interest: the .csv
		if entry.endswith(".csv"):
			fp = open(DIR + entry, 'r', newline='')
			
			for _ in range(9): # Skip the first 9 lines. First 8 describe the measurements, 9th describes the layout (which is hardcoded)
				next(fp)
			
			print("Reformatted " + entry)
			data = hourlyAverage(fp) # !!! There are 2 entries in testing !!!

			graphing.graph(entry, data)
			print("Graphed " + entry)
			fp.close()
	
	print("Success!")
	print("All generated graphs can be found in the 'output' folder.")



