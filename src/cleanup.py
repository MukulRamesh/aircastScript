from os import listdir
import csv
import datetime
from pytimeparse import parse
import graphing
import publicdata

DIR = "./temp/"

# PERIOD = datetime.timedelta(days=14) # The last x amount of time that I am extracting

# TICKER = datetime.timedelta(hours=1) # How the data is delineated: average by x amount of time

# Hard coded field names because the CSV file is badly formatted
fieldNames = ['ObjectID', 'Session_Name', 'Timestamp', 'Latitude', 'Longitude', 'Fahrenheit', 'PM1', 'PM10', 'PM2.5', '3-RH']

def hourlyAverage(fp, PERIOD, TICKER, includeOpenAQ):

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

	try:
		while curStamp > earliestStamp:
			periodData.append(lis[i])

			i = i - 1
			curStamp = lis[i][0]
	except IndexError:
		missingDataTime = curStamp - earliestStamp
		print("WARN: The PERIOD was larger than the dataset by " + str(missingDataTime) + ". Graphing the entire data set instead.")

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


	if includeOpenAQ:
		publicList = publicdata.getOpenAQ("day", str(mostRecentStamp), str(earliestStamp))
	else:
		publicList = None

	return averagedList, publicList


def makeCleanGraph(periodLengthStr, averageLengthStr, intervalLengthStr, dotIntervalLengthStr, includeTitle, includeOpenAQ):
	entries = listdir(DIR)
	period = datetime.timedelta(seconds=parse(periodLengthStr))
	average_block = datetime.timedelta(seconds=parse(averageLengthStr))

	# These both need to be in a "number of hours" integer
	interval = int(parse(intervalLengthStr) / 3600)
	dotInterval = int(parse(dotIntervalLengthStr) / 3600)



	for entry in entries: # I assume that every zip file has only one point of interest: the .csv
		if entry.endswith(".csv"):
			fp = open(DIR + entry, 'r', newline='')

			# Skip the first 9 lines. First 8 describe the measurements, 9th describes the layout  (which is hardcoded)
			for _ in range(9):
				next(fp)

			print("Reformatted " + entry)

			data, publicList = hourlyAverage(fp, period, average_block, includeOpenAQ) #if includeOpenAQ == TRUE, then, publicList == None

			graphing.lineGraphDotted(entry, data, interval, dotInterval, includeTitle, publicList, includeOpenAQ)
			print("Graphed " + entry)
			fp.close()

	print("Success!")
	print("All generated graphs can be found in the 'output' folder.")



