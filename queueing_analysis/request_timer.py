import requests

def calculateAverage(requestTimes):
	total = 0
	for time in requestTimes:
		total += time

	return total / len(requestTimes)

myServerRequestTimes = []
lightSErverRequestTimes = []

for i in range(0,100):
	time = requests.get("http://localhost:3000/index.html").elapsed.total_seconds()
	#print time
	myServerRequestTimes.append(time)

print "my python server average:", calculateAverage(myServerRequestTimes)


for i in range(0,100):
	time = requests.get("http://localhost:3003/index.html").elapsed.total_seconds()
	#print time
	lightSErverRequestTimes.append(time)

print "lighttpd server average:", calculateAverage(lightSErverRequestTimes)