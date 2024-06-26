import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import figure
import datetime

def graph(name, data):
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