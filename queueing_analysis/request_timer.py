import requests
import matplotlib.pyplot as plt

def calculateAverage(requestTimes):
	total = 0
	for time in requestTimes:
		total += time

	return total / len(requestTimes)

myServerRequestTimes = []
lightSErverRequestTimes = []

for i in range(0,100):
	url = "http://localhost:3000/file" + str(999 - i) + ".txt"
	url1 = "http://localhost:3000/index.html"
	time = requests.get(url).elapsed.total_seconds()
	myServerRequestTimes.append(time)

for i in range(0,100):
	url = "http://localhost:3000/file" + str(999 - i) + ".txt"
	url1 ="http://localhost:3003/index.html"
	time = requests.get(url).elapsed.total_seconds()
	lightSErverRequestTimes.append(time)

myAvgReqTime = calculateAverage(myServerRequestTimes)
lightAvgReqTime = calculateAverage(lightSErverRequestTimes)

print "my python server average:   ", myAvgReqTime
print "myServiceRatePerSec:        ", 1 / myAvgReqTime
print "------------------------------------------------"
print "lighttpd server average:    ", lightAvgReqTime
print "lighttpdServiceRatePerSec:  ", 1 / lightAvgReqTime



def plotData(mu):
	x = []
	y = []
	for lmbda in range(0, int(mu)):
		utilization = lmbda / mu
		avgTimeInSystem = 1 / (mu - lmbda)
		print utilization, avgTimeInSystem
		x.append(avgTimeInSystem)
		y.append(utilization)

	plt.plot(y,x)



myMu = 1 / myAvgReqTime
lightMu = 1 / lightAvgReqTime



plt.figure(1)

# plt.plot([1,2,3,4],[2,2,2,2])
# plt.plot([1,4,5,6])
plotData(myMu)
plotData(lightMu)
plt.legend(["My Python Web Server", "LightTPD Server"])
plt.ylabel('Average Time in System')
plt.xlabel('Utilization')
plt.show()

