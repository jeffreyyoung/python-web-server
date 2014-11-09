import optparse
import sys

import matplotlib
matplotlib.use('Agg')
from pylab import *

from myGenerator import WorkloadGenerator

# Class that parses a file and plots several graphs
class Plotter:
    def __init__(self):
        self.data = {}
        self.sizes = {}
        pass

    def parse(self,loglines, utilization):
        print "utilization!!!! ", utilization
        """ Parse the data file and accumulate values for plots. 
        """
        # Initialize plotter variables.
		# open file

        for line in loglines:
			# skip lines starting with a comment character
            if line.startswith("#"):
                continue
			# try parsing the line
            try:
                id, url,statuscode,somethingelse,size,seconds = line.split()
            except:
                continue
			# convert to proper data types

            threads = int(utilization)
            size = int(size)
            seconds = float(seconds)
			# add to dictionary
            if threads not in self.data:
                self.data[threads] = []
            self.data[threads].append(seconds)

    def plot(self,name):
		clf()
		# plot download times
		x = []
		keys = []
		# collect data into a list of lists
		for threads in sorted(self.data.keys()):
			x.append(self.data[threads])
			keys.append(threads)
		# plot all the lists as a boxplot
		boxplot(x,positions=keys)
		xlabel('Utilization')
		ylabel('Average Time in System-Data')
		savefig('download-time-%s.png' % name)

def doStuff(p, host, port, maxload):
    loadInc = maxload/10
    for i in range (0,3):
        wg = WorkloadGenerator(host, port, loadInc * i + 10)
        wg.startDuration(3)
        p.parse(wg.getLines(), loadInc * i)
        #wg.flushLines();

if __name__ == '__main__':
    p = Plotter()
    # wg = WorkloadGenerator("localhost", 3000, 1000)
    # wg.startDuration(10)
    # p.parse(wg.getLines(), 100)
    # wg.flushLines();
    doStuff(p, "localhost", 3000, 1000)

    p.plot('thing')

