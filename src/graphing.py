import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import figure
import itertools

# lengths of time of values below ARE IN HOURS
# interval = 24
# dotInterval = 12

def lineGraph(name, data):
	fig = figure(figsize=(40, 12), dpi=300)
	ax = plt.gca()

	x = [d[0] for d in data]
	y = [d[1] for d in data]
	


	ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d - %H:00'))
	ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
	
	ax.set_ylabel('PM2.5 microgram per cubic meter')
	ax.set_xlabel('Date - Time')

	ax.set_ylim([min(y) - 1, max(max(y), 125)])

	ax.axhspan(0, 50, xmin=0, xmax=1, facecolor='palegreen')
	ax.axhspan(51, 100, xmin=0, xmax=1, facecolor='yellow')
	ax.axhspan(101, 150, xmin=0, xmax=1, facecolor='orange')
	ax.axhspan(151, 200, xmin=0, xmax=1, facecolor='red')
	ax.axhspan(201, 300, xmin=0, xmax=1, facecolor='purple')
	ax.axhspan(301, 500, xmin=0, xmax=1, facecolor='maroon')



	plt.plot(x,y, linewidth=5.0)
	plt.gcf().autofmt_xdate()
	plt.savefig('./output/' + name + '.png', bbox_inches='tight')
	
	plt.close(fig)

def lineGraphDotted(name, data, interval, dotInterval):
	
	fig = figure(figsize=(15, 12), dpi=300)
	ax = plt.gca()

	x = [d[0] for d in data]
	y = [d[1] for d in data]
	
	markerColorList = []
	for val in y:
		if val > 301:
			markerColorList.append("maroon")
		elif val > 201:
			markerColorList.append("purple")
		elif val > 151:
			markerColorList.append("red")
		elif val > 101:
			markerColorList.append("orange")
		elif val > 51:
			markerColorList.append("yellow")
		else:
			markerColorList.append("palegreen")

	markerColorIter = itertools.cycle(markerColorList)


	ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
	ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
	
	ax.set_ylabel('PM2.5 microgram per cubic meter')
	ax.set_xlabel('Date')

	yRange = [0, max(max(y) + 30, 70)]
	ax.set_ylim(yRange)
	
	plt.plot(x,y, linewidth=2.0, color="grey") # plot line

	i = 0
	for x1,y1 in zip(x,y):
		color = next(markerColorIter)
		if i % int(dotInterval) == 0:
			plt.plot(x1,y1, marker='o', markersize=10, markerfacecolor=color, markeredgecolor=color) # plot dots
			
			textScale = ((yRange[1] - yRange[0]) / 100) * 3
			ax.text(x1, y1+textScale, "%d" %y1, ha="center") # write text value above dots
		i += 1
	
	
	plt.gcf().autofmt_xdate()
	plt.savefig('./output/' + name + '.png', bbox_inches='tight')
	
	plt.close(fig)

def graph(name, data, interval, dotInterval):
	# lineGraph(name, data)
	lineGraphDotted(name, data, interval, dotInterval)

