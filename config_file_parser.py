class ParsedConfigFile:
	def __init__(self):
		self.medias = {};
		self.hosts = {};
		self.parameters = {};
		self.parseConfigFile();
	def parseConfigFile(self):
		with open('web.conf') as f:
			for line in f:
				self.parseLine(line.rstrip())
	def parseLine(self, line):
		words = line.split(" ", 2)
		if "host" in words[0]:
			self.hosts[words[1]] = words[2]
		elif "media" in words[0]:
			self.medias[words[1]] = words[2]
		elif "parameter" in words[0]:
			self.parameters[words[1]] = words[2]

#ParsedConfigFile()